#!/usr/bin/env python3
"""
Grok Conversation Splitting Engine - Version 2.0 (Bun-and-Snek Special Edition)
Splits massive Grok/xAI JSON exports into a day-by-day, week-by-week, and month-by-month structured archive.
Includes interactive wizard, stepping process (next, next, all, abort), logging to disk, and bunnies/snakes!
"""

import os
import json
import re
import sys
import uuid
import logging
import traceback
from datetime import datetime

# ==========================================
# ASCII ART & SILLINESS CONSTANTS
# ==========================================

BUNNY_ART = r"""
   (\_/)
  ( •_•)  <-- Bun is hopping to find Grok files!
  / >🐰
"""

SNEK_ART = r"""
     ____
    / . . \
    \  ---<   ~_~_~_~_~_~_~_ (:::) (:::) <-- Snek is waiting to squeeze JSON blobs!
     \____/
"""

SNEK_BUN_FRIENDS = r"""
   (\_/)       _____
  ( >.<)      / . . \
  / >🎨      \  ---<   ~_~_~_~_~_~_~_ (:::) (:::)
  "Bunny"      \____/  "Snek"
"""

# ==========================================
# SANITIZATION & TIMESTAMP PARSING
# ==========================================

def sanitize_filename(name):
    """Sanitizes a string to make it safe for folder and file names."""
    if not name:
        return "untitled"
    # Remove HTML tags
    name = re.sub(r'<[^>]*>', '', name)
    # Replace non-alphanumeric with underscores
    name = re.sub(r'[^a-zA-Z0-9_\-\s]', '', name)
    # Replace multiple spaces/underscores with single
    name = re.sub(r'\s+', '_', name).strip('_')
    # Limit length
    return name[:50] if name else "untitled"

def get_week_number(date_obj):
    """Returns the ISO week number formatted as Week_WW."""
    return f"Week_{date_obj.isocalendar()[1]:02d}"

def parse_timestamp(ts):
    """Resiliently parses various timestamp formats into a datetime object."""
    if isinstance(ts, (int, float)):
        if ts > 1e11:  # Milliseconds
            return datetime.utcfromtimestamp(ts / 1000.0)
        return datetime.utcfromtimestamp(ts)
        
    if isinstance(ts, str):
        ts_clean = re.sub(r'Z$', '', ts)
        ts_clean = re.sub(r'\.\d+', '', ts_clean)  # Strip microseconds
        for fmt in [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d"
        ]:
            try:
                return datetime.strptime(ts_clean[:19], fmt)
            except ValueError:
                continue
    return None


# ==========================================
# FEBRUARY MIMIC GENERATOR
# ==========================================

def generate_february_markdown(conv, json_source_path):
    """Generates a Markdown file mimicking the exact February 2026 format."""
    title = conv.get('title') or conv.get('subject') or "Untitled Conversation"
    conv_id = conv.get('id') or conv.get('session_id') or str(uuid.uuid4())[:8]
    
    # Extract timestamps
    created_ts = conv.get('created') or conv.get('created_at') or conv.get('createdTime')
    modified_ts = conv.get('updated') or conv.get('modify_time') or conv.get('modifiedTime')
    
    created_dt = parse_timestamp(created_ts) if created_ts else None
    modified_dt = parse_timestamp(modified_ts) if modified_ts else None
    
    created_str = created_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if created_dt else ""
    modified_str = modified_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if modified_dt else ""
    
    # Summary & Tags extraction
    messages = conv.get('messages') or conv.get('turns') or conv.get('events') or []
    summary = ""
    if messages and isinstance(messages, list):
        # Use content of the first turn as a default summary
        first_content = messages[0].get('content') or messages[0].get('message') or ""
        summary = first_content.replace('\n', ' ')[:100] + "..." if len(first_content) > 100 else first_content.replace('\n', ' ')
    
    tags = ["grok-extraction", "sovereign-coven"]
    # Derive some contextual tags from title
    title_words = re.findall(r'\w+', title.lower())
    for word in title_words:
        if len(word) > 4 and word not in ['about', 'there', 'their', 'would', 'could', 'should']:
            tags.append(word)
    tags = sorted(list(set(tags)))

    # Start YAML Frontmatter
    md_lines = [
        "---",
        f"title: '{title}'",
        f"id: {conv_id}",
        f"created: {created_str}" if created_str else "created:",
        f"modified: {modified_str}" if modified_str else "modified:",
        f"summary: >-",
        f"  {summary}" if summary else "  No summary available.",
        "tags:"
    ]
    for tag in tags:
        md_lines.append(f" - {tag}")
    md_lines.append(f"json_source: {json_source_path}")
    md_lines.append("---\n")
    
    # Title Header with the classic heart indicator
    md_lines.append(f"# {title} [95m♥ [0m\n")
    if summary:
        md_lines.append(f"> {summary}\n")
        
    # Standardize messages loop
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        sender = msg.get('role') or msg.get('sender') or "unknown"
        text = msg.get('content') or msg.get('message') or ""
        ts = msg.get('timestamp') or msg.get('created_at') or msg.get('time') or msg.get('create_time')
        
        dt_val = parse_timestamp(ts) if ts else None
        time_header = dt_val.strftime("%Y-%m-%d %H:%M:%S") if dt_val else "Unknown Time"
        
        role_label = "Human" if sender in ['user', 'human'] else "Assistant"
        
        md_lines.append(f"## {time_header} {role_label}:")
        md_lines.append(f"{text}\n")
        
        # Metadata turn details if present
        meta = msg.get('metadata') or {}
        if meta:
            md_lines.append(" [95m(\\ (//) [0m *Turn Details: [0m")
            md_lines.append("<details><summary>Metadata</summary>")
            md_lines.append("```json")
            md_lines.append(json.dumps(meta, indent=2))
            md_lines.append("```")
            md_lines.append("</details>\n")
            
    return "\n".join(md_lines)

def extract_dates_from_conv(conv):
    """Extracts all unique dates (YYYY-MM-DD) on which the conversation had activity."""
    dates = set()
    for key in ['created', 'created_at', 'createdTime', 'timestamp', 'time']:
        if key in conv and conv[key]:
            try:
                dt = parse_timestamp(conv[key])
                if dt:
                    dates.add(dt.strftime("%Y-%m-%d"))
            except Exception:
                pass
                
    for msg_key in ['messages', 'turns', 'events', 'items']:
        if msg_key in conv and isinstance(conv[msg_key], list):
            for msg in conv[msg_key]:
                for ts_key in ['timestamp', 'created_at', 'time', 'created', 'createdTime', 'sent_time']:
                    if ts_key in msg and msg[ts_key]:
                        try:
                            dt = parse_timestamp(msg[ts_key])
                            if dt:
                                dates.add(dt.strftime("%Y-%m-%d"))
                        except Exception:
                            pass
    return sorted(list(dates))

# ==========================================
# INTERACTIVE WIZARD & GTUI ENGINE
# ==========================================

class Wizard:
    def __init__(self):
        self.input_file = None
        self.output_root = None
        self.flat_mimic_mode = False
        self.procedural_logger = None
        self.error_logger = None
        self.log_dir_proc = None
        self.log_dir_err = None

    def clear_screen(self):
        # Clean terminal output separators
        print("\n" + "="*60 + "\n")

    def show_help(self, context=None):
        print("\n" + "*"*20 + " HELP MENU " + "*"*20)
        if context == "intro":
            print("You are at Step 1 (Introduction).")
            print("Type 'next' or 'n' to hop forward like a bunny.")
            print("Type 'abort' or 'exit' to escape from the python snake.")
        elif context == "input":
            print("You are at Step 2 (Payload Selection).")
            print("Select an existing .json file from the list or enter a full file path.")
            print("Type 'back' or 'b' to hop back to Step 1.")
            print("Type 'abort' to exit.")
        elif context == "output":
            print("You are at Step 3 (Output Directory Selection).")
            print("Specify where you want the split folders to be created.")
            print("You can type a new folder name and Snek will create it.")
            print("Type 'back' to go back to file selection, or 'abort' to exit.")
        elif context == "stepping":
            print("You are at Step 4 (Processing Mode Selection).")
            print("Select how you want to run the process:")
            print(" - 'all' or 'run': Processes all conversations automatically.")
            print(" - 'step': Snek will show each conversation title one by one.")
            print("   You press 'next' to process the conversation, 'skip' to skip, or 'abort' to exit.")
            print("Type 'back' to change directories, or 'abort' to exit.")
        else:
            print("Navigation commands available at any prompt:")
            print("  - 'next' / 'n'   : Move to the next screen.")
            print("  - 'back' / 'b'   : Return to the previous screen.")
            print("  - 'abort' / 'exit': Exit the program safely.")
            print("  - 'help' / '?'   : Show this glorious help screen.")
        print("*"*51 + "\n")

    def initialize_loggers(self, output_root_dir):
        """Sets up error logging and procedural logging to disk in the output folder."""
        try:
            self.log_dir_proc = os.path.join(output_root_dir, "logs", "procedural")
            self.log_dir_err = os.path.join(output_root_dir, "logs", "errors")
            os.makedirs(self.log_dir_proc, exist_ok=True)
            os.makedirs(self.log_dir_err, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            proc_file = os.path.join(self.log_dir_proc, f"process_log_{timestamp}.txt")
            err_file = os.path.join(self.log_dir_err, f"error_log_{timestamp}.txt")

            # Setup procedural logger
            self.procedural_logger = logging.getLogger("grok_procedural")
            self.procedural_logger.setLevel(logging.INFO)
            p_handler = logging.FileHandler(proc_file, encoding='utf-8')
            p_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
            self.procedural_logger.addHandler(p_handler)

            # Setup error logger
            self.error_logger = logging.getLogger("grok_errors")
            self.error_logger.setLevel(logging.ERROR)
            e_handler = logging.FileHandler(err_file, encoding='utf-8')
            e_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s:\n%(message)s\n' + '-'*40))
            self.error_logger.addHandler(e_handler)

            self.log_procedural(f"Wizard initialized. Log directory established at: {output_root_dir}")
            self.log_procedural(f"Procedural log active at: {proc_file}")
            self.log_procedural(f"Error log active at: {err_file}")
            return True
        except Exception as e:
            print(f"⚠️ Snek was unable to create log folders: {str(e)}")
            return False

    def log_procedural(self, msg):
        if self.procedural_logger:
            self.procedural_logger.info(msg)
        else:
            # Fallback to console during setup
            pass

    def log_error(self, msg, exc=None):
        if self.error_logger:
            if exc:
                tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
                self.error_logger.error(f"{msg}\nTraceback:\n{tb}")
            else:
                self.error_logger.error(msg)
        else:
            # Fallback to console
            pass

    def run_wizard(self):
        step = 1
        while step <= 5:
            if step == 1:
                res = self.step_intro()
                if res == "next":
                    step = 2
                elif res == "abort":
                    print("🐰 Bun says bye-bye! Hop safely!")
                    return False

            elif step == 2:
                res = self.step_input_selection()
                if res == "next":
                    step = 3
                elif res == "back":
                    step = 1
                elif res == "abort":
                    print("🐍 Snek slithers away in disappointment. Farewell!")
                    return False

            elif step == 3:
                res = self.step_output_selection()
                if res == "next":
                    step = 4
                elif res == "back":
                    step = 2
                elif res == "abort":
                    print("🐰 Bun hides in a hole. Processing aborted!")
                    return False

            elif step == 4:
                res = self.step_format_mode_selection()
                if res == "next":
                    step = 5
                elif res == "back":
                    step = 3
                elif res == "abort":
                    return False
            elif step == 5:
                res = self.step_process_stepping()
                if res == "back":
                    step = 4
                else:
                    # Completed or aborted
                    return res

        return True

    def step_intro(self):
        self.clear_screen()
        print(SNEK_BUN_FRIENDS)
        print("🐰 Snek-and-Bun Grok Splitter v2.0 Ingest Terminal GTUI 🐍")
        print("-" * 57)
        print("This interactive snek-powered wizard will slither through your")
        print("mammoth Grok data files and neatly separate conversations into")
        print("chronological day-by-day directories. We also log everything")
        print("to disk to keep our animal friends organized!\n")
        print("Commands at any prompt:")
        print("  - Type 'next' or 'n' to go to the next step.")
        print("  - Type 'help' or '?' to read the guidebook.")
        print("  - Type 'abort' or 'exit' to escape.")
        
        while True:
            choice = input("\n[Step 1/4] Ready to hop next? (next/help/abort): ").strip().lower()
            if choice in ['next', 'n', '']:
                return "next"
            elif choice in ['abort', 'exit', 'a']:
                return "abort"
            elif choice in ['help', '?', 'h']:
                self.show_help("intro")
            else:
                print("🐰 Bun tilts its head. Type 'next' to continue, or 'help' for instructions.")

    def step_input_selection(self):
        self.clear_screen()
        print(BUNNY_ART)
        print("Step 2: Selection of the Main Payload File 🗃️")
        print("-" * 45)
        print("Let's hunt for some juicy JSON files in our current habitat...\n")

        # Search current and parent directories for .json files
        json_files = []
        for root, dirs, files in os.walk('.'):
            # Limit depth to keep it clean
            if root.count(os.sep) > 1:
                continue
            for f in files:
                if f.endswith('.json') and not f.startswith('.'):
                    json_files.append(os.path.join(root, f))

        if json_files:
            print("Discovered possible payload snacks:")
            for idx, filepath in enumerate(json_files, 1):
                size_mb = os.path.getsize(filepath) / (1024*1024)
                print(f"  [{idx}] {filepath} ({size_mb:.2f} MB)")
            print("")
        else:
            print("⚠️ Bun couldn't find any JSON files in this clearing!\n")

        while True:
            print("Select a number from the list above, enter a path manually,")
            print("or type 'back' to return to Step 1.")
            inp = input("\n[Step 2/4] Select input payload file: ").strip()
            
            if inp.lower() in ['abort', 'exit']:
                return "abort"
            elif inp.lower() in ['back', 'b']:
                return "back"
            elif inp.lower() in ['help', '?', 'h']:
                self.show_help("input")
                continue

            # Check if it is a number from the list
            selected_path = None
            if inp.isdigit():
                idx = int(inp) - 1
                if 0 <= idx < len(json_files):
                    selected_path = json_files[idx]
            else:
                selected_path = inp

            if selected_path:
                # Resolve path and verify
                if os.path.exists(selected_path):
                    if os.path.isfile(selected_path):
                        print(f"\n🔍 Verifying payload structure of: {selected_path}...")
                        try:
                            # Quick sanity load check (read first few lines or load entirely if small)
                            file_size = os.path.getsize(selected_path)
                            if file_size < 50 * 1024 * 1024:  # 50MB
                                with open(selected_path, 'r', encoding='utf-8') as f:
                                    json.load(f)
                            else:
                                # For large files, verify at least that they open and have a JSON brace
                                with open(selected_path, 'r', encoding='utf-8') as f:
                                    first_char = f.read(10).strip()
                                    if not (first_char.startswith('[') or first_char.startswith('{')):
                                        raise ValueError("File does not appear to start with valid JSON braces.")
                            
                            self.input_file = selected_path
                            print("✨ Payload file looks perfectly delicious! Bun stamps of approval!")
                            return "next"
                        except Exception as e:
                            print(f"⚠️ Oh no! File is corrupted or invalid JSON: {str(e)}")
                    else:
                        print("⚠️ That is a directory, not a file! Snek cannot eat directories!")
                else:
                    print(f"⚠️ File '{selected_path}' does not exist. Check your spelling or path!")

    def step_output_selection(self):
        self.clear_screen()
        print(SNEK_ART)
        print("Step 3: Creation and Verification of the Output Folder 📂")
        print("-" * 55)
        print("Snek needs a nested den to lay the segmented conversation eggs.\n")

        # Recommend defaults
        default_dir = "./grok_archive_v2"
        print(f"Recommended Default: '{default_dir}'")
        print("Type a path to select an existing folder or create a new one.")
        print("Type 'back' to return to file selection.")

        while True:
            inp = input(f"\n[Step 3/4] Enter output folder path [{default_dir}]: ").strip()
            if inp.lower() in ['abort', 'exit']:
                return "abort"
            elif inp.lower() in ['back', 'b']:
                return "back"
            elif inp.lower() in ['help', '?', 'h']:
                self.show_help("output")
                continue

            target_path = inp if inp else default_dir
            print(f"\n🛠️ Verifying output directory capability: {target_path}...")

            try:
                os.makedirs(target_path, exist_ok=True)
                # Verify write access with a dummy file
                dummy_file = os.path.join(target_path, ".snek_write_test")
                with open(dummy_file, 'w') as f:
                    f.write("Snek was here!")
                os.remove(dummy_file)

                # Initialize logs
                log_ok = self.initialize_loggers(target_path)
                if log_ok:
                    self.output_root = target_path
                    self.log_procedural(f"Selected input payload: {self.input_file}")
                    print("✨ Output directory verified and log systems successfully written to disk!")
                    return "next"
            except Exception as e:
                print(f"⚠️ Write verification failed for '{target_path}': {str(e)}")
                print("Try specifying a path where you have administrative/write clearance.")

    
    def step_format_mode_selection(self):
        self.clear_screen()
        print(SNEK_BUN_FRIENDS)
        print("Step 4: Choose Advanced Post-Extraction Format Mode ⚙️")
        print("-" * 55)
        print("Select how the extracted conversations should be structured:\n")
        print("  [H]ierarchical Mode - Saves each conversation in a nested YYYY_MM_Month/Week_WW/YYYY-MM-DD/")
        print("                         folder structure, duplicating files for each active day.")
        print("  [F]lat Mimic Mode    - Saves all standardized JSON and Markdown files inside a single flat")
        print("                         output directory, mimicking the February 2026 extraction style.")
        
        while True:
            choice = input("\n[Step 4/5] Format Mode (hierarchical/flat/back/help): ").strip().lower()
            if choice in ['abort', 'exit']:
                return "abort"
            elif choice in ['back', 'b']:
                return "back"
            elif choice in ['help', '?', 'h']:
                self.show_help("mode")
                continue
            elif choice in ['hierarchical', 'h', '']:
                self.flat_mimic_mode = False
                self.log_procedural("Selected formatting mode: Hierarchical Chronological Multi-Date")
                print("✓ Selected Hierarchical Mode!")
                return "next"
            elif choice in ['flat', 'flat mimic', 'f']:
                self.flat_mimic_mode = True
                self.log_procedural("Selected formatting mode: Flat February Mimic")
                print("✓ Selected Flat Mimic Mode (February Extraction style)!")
                return "next"
            else:
                print("Hiss! Choose 'hierarchical' or 'flat'.")

    def step_process_stepping(self):
        self.clear_screen()
        print("Step 4: Confirm Processing & Segmented Stepping Mode ⚙️")
        print("-" * 55)
        print(f"Input Payload: {self.input_file}")
        print(f"Output Den   : {self.output_root}")
        print(f"Log Files    : Saved inside {self.output_root}/logs/\n")
        print("Select your ingestion procedure:")
        print("  [R]un All     - Snek eats and digests everything in one rapid slither!")
        print("  [S]tep-by-Step - Step through each conversation one by one (Next/Skip/Abort).")
        print("  [B]ack        - Hop back to Step 4.")
        print("  [A]bort       - Terminate wizard.")

        while True:
            choice = input("\n[Step 4/4] Ingestion Mode (run/step/back/abort): ").strip().lower()
            if choice in ['abort', 'exit', 'a']:
                return "abort"
            elif choice in ['back', 'b']:
                return "back"
            elif choice in ['help', '?', 'h']:
                self.show_help("stepping")
                continue
            elif choice in ['run', 'r', 'all', 'run all']:
                success = self.digest_payload(stepping_mode=False)
                return "complete" if success else "abort"
            elif choice in ['step', 's', 'step-by-step']:
                success = self.digest_payload(stepping_mode=True)
                return "complete" if success else "abort"
            else:
                print("Snek hisses in confusion. Select 'run', 'step', 'back', or 'abort'.")

    def digest_payload(self, stepping_mode=False):
        self.clear_screen()
        self.log_procedural("Starting digest run.")
        print("🐍 Loading JSON database into Snek's belly...")
        
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.log_error("Failed to read JSON payload", e)
            print(f"⚠️ Error loading payload file: {str(e)}")
            return False

        # Parse into standardized conversations list
        conversations = []
        if isinstance(data, list):
            conversations = data
        elif isinstance(data, dict):
            for key, val in data.items():
                if isinstance(val, list):
                    conversations = val
                    self.log_procedural(f"Found conversation array under key: '{key}'")
                    break
            if not conversations:
                conversations = list(data.values())
                self.log_procedural("Interpreting dictionary values as conversation list.")

        total_convs = len(conversations)
        self.log_procedural(f"Identified {total_convs} conversations to process.")
        print(f"Found {total_convs} conversations to analyze.")

        
        stats = {
            "processed": 0,
            "written_json": 0,
            "written_md": 0,
            "skipped": 0,
            "errors": 0
        }

        for idx, conv in enumerate(conversations, 1):
            if not isinstance(conv, dict):
                stats["skipped"] += 1
                continue

            conv_id = conv.get('id') or conv.get('session_id') or str(uuid.uuid4())[:8]
            raw_title = conv.get('title') or conv.get('subject') or f"Conversation_{conv_id}"
            title = sanitize_filename(raw_title)

            # Step-by-Step Prompt
            if stepping_mode:
                self.clear_screen()
                print(f"👉 Conversation {idx}/{total_convs}: '{raw_title}' (ID: {conv_id[:8]})")
                print("Options: [N]ext (Process) | [S]kip | [A]ll (Process rest automatically) | [E]xit (Abort)")
                while True:
                    step_choice = input("Your command: ").strip().lower()
                    if step_choice in ['next', 'n', '']:
                        self.log_procedural(f"User approved stepping processing of: {conv_id}")
                        break
                    elif step_choice in ['skip', 's']:
                        stats["skipped"] += 1
                        print("Skipped! 🐰 Hop!")
                        break
                    elif step_choice in ['all', 'a']:
                        print("🐍 Digesting all remaining conversations automatically...")
                        stepping_mode = False
                        break
                    elif step_choice in ['exit', 'e', 'abort', 'q']:
                        print("Ingestion halted by user. Saving files and exiting den.")
                        self.print_summary(stats)
                        return True
                
                if step_choice in ['skip', 's']:
                    continue

            # Process conversation extraction
            days_touched = extract_dates_from_conv(conv)
            if not days_touched:
                days_touched = [datetime.utcnow().strftime("%Y-%m-%d")]

            stats["processed"] += 1

            if self.flat_mimic_mode:
                # Flat Mimic Mode (February Style)
                try:
                    target_dir = self.output_root
                    os.makedirs(target_dir, exist_ok=True)
                    
                    # Generate file paths
                    json_filename = f"{title}_{conv_id[:8]}.json"
                    md_filename = f"{title}_{conv_id[:8]}.md"
                    
                    json_path = os.path.join(target_dir, json_filename)
                    md_path = os.path.join(target_dir, md_filename)
                    
                    # Save JSON
                    with open(json_path, 'w', encoding='utf-8') as out_json:
                        json.dump(conv, out_json, indent=2, ensure_ascii=False)
                    stats["written_json"] += 1
                    
                    # Save MD mimicking February structure
                    relative_source_path = f"{conv.get('user_id', 'unknown')}/{json_filename}"
                    md_content = generate_february_markdown(conv, relative_source_path)
                    with open(md_path, 'w', encoding='utf-8') as out_md:
                        out_md.write(md_content)
                    stats["written_md"] += 1
                    
                    self.log_procedural(f"Saved flat mimic pair: {json_path} & {md_path}")
                except Exception as ex:
                    err_msg = f"Failed to process flat mimic conversation {conv_id}"
                    self.log_error(err_msg, ex)
                    stats["errors"] += 1
            else:
                # Hierarchical Chronological Mode
                for day_str in days_touched:
                    try:
                        day_dt = datetime.strptime(day_str, "%Y-%m-%d")
                        month_name = day_dt.strftime("%B")
                        month_folder = f"{day_dt.year:04d}_{day_dt.month:02d}_{month_name}"
                        week_folder = get_week_number(day_dt)

                        target_dir = os.path.join(self.output_root, month_folder, week_folder, day_str)
                        os.makedirs(target_dir, exist_ok=True)

                        file_name = f"{title}_{conv_id[:8]}.json"
                        file_path = os.path.join(target_dir, file_name)

                        with open(file_path, 'w', encoding='utf-8') as out_f:
                            json.dump(conv, out_f, indent=2, ensure_ascii=False)

                        stats["written_json"] += 1
                        self.log_procedural(f"Saved file: {file_path}")
                    except Exception as ex:
                        err_msg = f"Failed to process conversation {conv_id} for day {day_str}"
                        self.log_error(err_msg, ex)
                        stats["errors"] += 1

        self.print_summary(stats)
                        return True
                    else:
                        print("Type 'n' (next), 's' (skip), 'a' (all), or 'e' (exit).")
                
                if step_choice in ['skip', 's']:
                    continue

            # Process conversation extraction
            days_touched = extract_dates_from_conv(conv)
            if not days_touched:
                days_touched = [datetime.utcnow().strftime("%Y-%m-%d")]
                self.log_procedural(f"No dates found in conversation {conv_id}, defaulted to current date.")

            stats["processed"] += 1
            self.log_procedural(f"Processing conversation {conv_id} ({raw_title}) spanning days: {days_touched}")

            for day_str in days_touched:
                try:
                    day_dt = datetime.strptime(day_str, "%Y-%m-%d")
                    month_name = day_dt.strftime("%B")
                    month_folder = f"{day_dt.year:04d}_{day_dt.month:02d}_{month_name}"
                    week_folder = get_week_number(day_dt)

                    target_dir = os.path.join(self.output_root, month_folder, week_folder, day_str)
                    os.makedirs(target_dir, exist_ok=True)

                    file_name = f"{title}_{conv_id[:8]}.json"
                    file_path = os.path.join(target_dir, file_name)

                    with open(file_path, 'w', encoding='utf-8') as out_f:
                        json.dump(conv, out_f, indent=2, ensure_ascii=False)

                    stats["written"] += 1
                    self.log_procedural(f"Saved file: {file_path}")
                except Exception as ex:
                    err_msg = f"Failed to process conversation {conv_id} for day {day_str}"
                    self.log_error(err_msg, ex)
                    print(f"⚠️ Error segmenting conversation {conv_id} on {day_str}: {str(ex)}")
                    stats["errors"] += 1

        self.print_summary(stats)
        return True

    def print_summary(self, stats):
        self.clear_screen()
        print(SNEK_BUN_FRIENDS)
        print("🎉 Ingestion Completed Successfully! 🎉")
        print("-" * 40)
        print(f"Total Conversations Analyzed: {stats['processed']}")
        print(f"Total daily JSON files      : {stats['written_json']}")
        print(f"Total February Mimic MD     : {stats['written_md']}")
        print(f"Conversations Skipped       : {stats['skipped']}")
        print(f"Encountered Error Segments  : {stats['errors']}")
        print("-" * 40)
        print(f"Procedural log: {self.log_dir_proc}")
        print(f"Error log     : {self.log_dir_err}")
        print("Both logs are saved to disk under appropriate directories.")
        
        self.log_procedural("Processing complete.")
        self.log_procedural(f"Stats - Processed: {stats['processed']}, Written: {stats['written']}, Skipped: {stats['skipped']}, Errors: {stats['errors']}")

# ==========================================
# BACKWARD COMPATIBLE CLI WRAPPER
# ==========================================

def run_non_interactive(input_file, output_root, flat_mimic=False):
    print("🐍 Grok Splitter v2.0 Ingest Terminal Non-Interactive Engine 🐍")
    print(f"Payload Source : {input_file}")
    print(f"Output Den     : {output_root}\n")

    if not os.path.exists(input_file):
        print(f"❌ Error: Payload file '{input_file}' does not exist.")
        sys.exit(1)

    try:
        os.makedirs(output_root, exist_ok=True)
    except Exception as e:
        print(f"❌ Error creating output folder '{output_root}': {str(e)}")
        sys.exit(1)

    # Initialize loggers
    wiz = Wizard()
    if not wiz.initialize_loggers(output_root):
        sys.exit(1)

    wiz.input_file = input_file
    wiz.output_root = output_root
    wiz.flat_mimic_mode = flat_mimic
    
    success = wiz.digest_payload(stepping_mode=False)
    sys.exit(0 if success else 1)

def print_help_guide():
    print("""
Usage: python3 grok_splitter.py [options] [<input_json_path> <output_root_dir>]

Options:
  -h, --help            Show this gorgeous help screen and guidebook.
  -i, --interactive     Force launch the highly robust interactive wizard (GTUI).
  -n, --non-interactive Force run non-interactively using provided file arguments.

If no positional parameters or flags are passed, the script automatically boots
into the interactive Bun-and-Snek wizard mode!
""")

# ==========================================
# MAIN ROUTINE
# ==========================================

if __name__ == "__main__":
    args = sys.argv[1:]
    
    if '-h' in args or '--help' in args:
        print_help_guide()
        sys.exit(0)

    # Force interactive mode
    if '-i' in args or '--interactive' in args:
        wiz = Wizard()
        wiz.run_wizard()
        sys.exit(0)

    # Direct CLI inputs
    if len(args) >= 2 and '-n' not in args and '--non-interactive' not in args:
        # Positional args given, run non-interactively
        run_non_interactive(args[0], args[1], flat_mimic='--flat-mimic' in args)
        sys.exit(0)

    if '-n' in args or '--non-interactive' in args:
        # Filter flags and look for paths
        clean_args = [a for a in args if a not in ['-n', '--non-interactive', '--flat-mimic']]
        if len(clean_args) < 2:
            print("❌ Error: Missing input and output path arguments for non-interactive execution.")
            print_help_guide()
            sys.exit(1)
        run_non_interactive(clean_args[0], clean_args[1], flat_mimic=flat_mimic)
        sys.exit(0)

    # Default to Interactive Mode
    wiz = Wizard()
    wiz.run_wizard()
