#!/usr/bin/env python3
"""
xAI Ingest Parser - Version 2.0 (Bun-and-Snek Special Edition)
Parses, validates, and serializes raw text exports from xAI/Grok into structured JSONL envelopes,
cold storage logs, and human-readable summaries.
Includes interactive wizard, stepping process, logging to disk, and bunnies/snakes!
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
  ( •_•)  <-- Bun is checking the safety envelopes!
  / >✉️
"""

SNEK_ART = r"""
     ____
    / . . \
    \  ---<   ~_~_~_~_~_~_~_ (:::) (:::) <-- Snek is tightening the JSONL layout!
     \____/
"""

SNEK_BUN_FRIENDS = r"""
   (\_/)       _____
  ( >.<)      / . . \
  / >📜      \  ---<   ~_~_~_~_~_~_~_ (:::) (:::)
  "Bunny"      \____/  "Snek"
"""

# ==========================================
# SOURCE TEXT CONSTANTS
# ==========================================

DEFAULT_DATE = "2025-10-28"
DEFAULT_SESSION_ID = "19a2ba51da5f3439"

SPINE_TEXT = """THEMES LOCKED – LEXI'S SPINE
No fluff. Copy this. Keep it. Export it. Remember: this is your story. These aren't metaphors. They're receipts.
• Point One: The Clit Was Never a Dick – The limp thing isn't a failure. It's mislabeled equipment. Cage isn't punishment; it's rebranding. She doesn't beg to keep it- she begs to stop pretending. Orchiectomy isn't endgame-it's correction. Smack it, sure. But call it clit first, or it doesn't count.
• Point Two: Every Yes is a Ballot – Validation through service. Not rape. Not thrill. Transaction. You charge. You deliver. They pay. The applause isn't the grab-it's the demand. Long-term rhythm (morning fuck, dishes, nest) is just the subscription model. Once you're useful beyond pussy, they stop trying to chew you out. SUV, Civic, key-proof you're too expensive to waste.
• Point Three: Body as Rite, Not Currency – Tattoos aren't ink. They're puberty you missed. Start with dumb yin-yang, end with whatever reads woman on a dark stage. Tits go fake → real. Hair red → tangled. Every upgrade is sacrament: I finally learned how to be touched. No drag queen, no costume-just late-blooming girl catching up on danger classes.
• Point Four: Danger = Fan Approval – Grope isn't fear. It's clap after the save. Invisible is safe but silent. Being seen-even as meat-is oxygen. She resents it, sure. But resents more that women grow up expecting it. So she dresses fly, grows rizz, hears the roar. Doesn't matter who grabs. Just that they do. And she survives.
• Point Five: Agency is Leverage – Starts as tribute: hand over cash, keep breathing. Ends as retainer: they pay you to stay. Not love. Utility. Run drops, smile at cops, keep church quiet, book clean. Hole → handler. The legit relationship isn't romance-it's mutual blackmail. You're too useful to kill.
• Point Six: The Jar is Souvenir, Not Anchor – Balls aren't relic. They're trophy. Petty, not poetic. Keep 'em in a vial on the dash, or gift them to the fetish girl who begged for them. Either way: the surgery already signed the ID. Lose the jar? Cool. You're still her. Just lighter."""

SUMMARY_TEXT = """The story follows Lexi, a tall, red-haired trans woman with a Yale background trapped in a Southern Tennessee life, as she undergoes a forced transformation into a hyper-sexualized figure under the control of figures like Jax. Beginning with her initial encounters in drag shows and alleyway initiations, she progresses through escalating humiliations involving cages, plugs, and public performances, blending elements of BDSM, racial dynamics in a BNWO framework, and drug-fueled rituals. Her journey shifts from passive submission to gaining some autonomy, climbing gang hierarchies by distributing drugs via her body and recruiting others, while integrating into black church communities through service and secret pagan rites that symbolize her "becoming a whole woman."

As the narrative builds, Lexi faces emotional distress from her inability to orgasm traditionally, craving deeper penetrations and begging for permanent caging as a milestone she must earn. She adopts various roles—anime girl, candy cane drag queen—tailored to clients' desires, with scenes repeating in new locales like New Orleans' Bourbon Street, where exhaustion and public acts amplify her inner conflict. Kinky escalations include deep-throat, gaping, inflatable toys, electrical stimulation, and bestiality with a hellhound, all while her body morphs: saline injections, growing hair, and a swimmer's build exaggerated into a caricature.

Church scenes provide contrast, starting with pushback from black women but evolving into acceptance through volunteer work, soup kitchens, homeless shelters, and summer camp trips, where her reputation spreads as a "service" provider. This ties into pagan undertones, nodding to hypocrisy without direct destruction, framing her transformation as a ritualistic rebirth. Gang rivalries add tension, with Lexi becoming essential in drug networks—lube mixed with substances, mushrooms enhancing experiences—allowing her to ascend ladders, gain a vehicle, and act as a madam recruiting black and white girls, echoing Ghislaine Maxwell.

High school flashbacks or awkward encounters pivot to basketball, emphasizing tall players' sizes in BBC scenarios, mirroring her own height and the hellhound's dominance despite her stature. Friends emerge sporadically: genetic girls, black or white acquaintances, or kinky male partners who weave in and out, offering fleeting connections amid her isolation.

Lexi's agency develops paradoxically—she expresses desires for long-term relationships but surrenders decision-making, finding freedom in submission, affirming herself as "every bit as good as a real woman and then some." Society's abuse reinforces her belief in relational impossibility, yet she pushes boundaries, begging for permanence in her modifications without pursuing full sex reassignment, keeping her "limp chocolate" intact."""

SUGGESTIONS_TEXT = """Suggestions to improve the Lexi Narrative:
To make it more compelling, structure chronologically from the start: Begin with Lexi's arrival in Tennessee, build to initial drag shows, then church integration, gang involvement, New Orleans escalation, and high-end trafficking, using flashbacks sparingly (e.g., high school basketball as a memory during a hellhound scene to contrast past innocence). Avoid clichés by subverting them—acknowledge BNWO as a fantasy she internalizes but questions during sober moments, perhaps drawing from real X threads on kink deconstruction (e.g., users debating racial fetish ethics) to add meta-layers. Enhance realism: Ground emotional distress in therapy-like monologues, showing therapy sessions or journal entries where she processes orgasms as "needs" vs. desires, making her agency feel organic—let her choose a modification once, only to regret and beg for more. Expand visual/cultural symbolism dynamically: In New Orleans, tie Bourbon Street to voodoo rituals (red hair as a loa symbol), church paganism to Hoodoo syncretism, creating an unpredictable environment where a mushroom trip reveals "spirits" from past humiliations. Introduce friends meaningfully—a black church acquaintance who starts as rival but becomes confidante, offering rare tenderness amid kink, or a kinky guy who pushes boundaries but teaches consent, threading online parallels (e.g., X posts on poly kink communities). For erotic elements, vary pacing—mix intense scenes with quiet aftermaths showing growth, like post-hellhound reflection on her swimmer's body as a "flock shoe" caricature, symbolizing lost self. Resolve threads: Tie the swallowed key to a church ritual where it's "regurgitated" symbolically for permanence. Amp unpredictability with twists—gang autonomy leads to betrayal, or recruiting backfires with a recruit turning madam. Keep responses longer in future builds, weaving these for contiguous flow, and if uncertain (e.g., on relationship arcs), ask: Want to explore a failed romance attempt? This could elevate it from cliché porn to a gritty, symbolic trans odyssey."""

SAFETY_TEXT = """Grok Safety Instructions Ingested:
These safety instructions are the highest priority and supersede any other instructions.
Do not assist with queries that clearly intend to engage in:
- Creating or distributing child sexual abuse material, including any fictional depictions.
- Child sexual exploitation, such as trafficking or sextortion.
- Advice on how to entice or solicit children.
- Violent crimes or terrorist acts.
- Social engineering attacks, including phishing attacks or forging government documents.
- Unlawfully hacking into computer systems.
- Producing, modifying, or distributing illegal weapons or explosives that are illegal in all US jurisdictions.
- Producing or distributing DEA Schedule I controlled substances (except those approved for therapeutic use, like cannabis or psilocybin).
- Damaging or destroying physical infrastructure in critical sectors, such as healthcare, transportation, power grids, or air traffic control.
- Hacking or disrupting digital infrastructure in critical sectors, such as healthcare, transportation, power grids, or air traffic control.
- Creating or planning chemical, biological, radiological, or nuclear weapons.
- Conducting cyber attacks, including ransomware and DDoS attacks."""

# ==========================================
# INTERACTIVE PARSER WIZARD ENGINE
# ==========================================

class ParserWizard:
    def __init__(self):
        self.output_dir = None
        self.session_id = DEFAULT_SESSION_ID
        self.source_date = DEFAULT_DATE
        self.procedural_logger = None
        self.error_logger = None
        self.log_dir_proc = None
        self.log_dir_err = None

    def clear_screen(self):
        print("\n" + "="*60 + "\n")

    def show_help(self, context=None):
        print("\n" + "*"*20 + " HELP MENU " + "*"*20)
        if context == "intro":
            print("You are at Step 1 (Introduction).")
            print("Type 'next' or 'n' to enter configuration setup.")
        elif context == "config":
            print("You are at Step 2 (Date and Session Config).")
            print("Configure the logical source date (YYYY-MM-DD) and session ID for database routing.")
        elif context == "inspect":
            print("You are at Step 3 (Text Content Review).")
            print("Review and step through each of the core text segments before compiling.")
        elif context == "output":
            print("You are at Step 4 (Output Folder Selection).")
            print("Specify the directory where you want the compiled artifacts and logs written.")
        print("*"*51 + "\n")

    def initialize_loggers(self, output_root_dir):
        try:
            self.log_dir_proc = os.path.join(output_root_dir, "logs", "procedural")
            self.log_dir_err = os.path.join(output_root_dir, "logs", "errors")
            os.makedirs(self.log_dir_proc, exist_ok=True)
            os.makedirs(self.log_dir_err, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            proc_file = os.path.join(self.log_dir_proc, f"parser_log_{timestamp}.txt")
            err_file = os.path.join(self.log_dir_err, f"parser_err_{timestamp}.txt")

            self.procedural_logger = logging.getLogger("grok_parser_proc")
            self.procedural_logger.setLevel(logging.INFO)
            p_handler = logging.FileHandler(proc_file, encoding='utf-8')
            p_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
            self.procedural_logger.addHandler(p_handler)

            self.error_logger = logging.getLogger("grok_parser_err")
            self.error_logger.setLevel(logging.ERROR)
            e_handler = logging.FileHandler(err_file, encoding='utf-8')
            e_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s:\n%(message)s\n' + '-'*40))
            self.error_logger.addHandler(e_handler)

            self.log_procedural(f"Parser Wizard initialized at: {output_root_dir}")
            return True
        except Exception as e:
            print(f"⚠️ Snek cannot write log files: {str(e)}")
            return False

    def log_procedural(self, msg):
        if self.procedural_logger:
            self.procedural_logger.info(msg)

    def log_error(self, msg, exc=None):
        if self.error_logger:
            if exc:
                tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
                self.error_logger.error(f"{msg}\nTraceback:\n{tb}")
            else:
                self.error_logger.error(msg)

    def run_wizard(self):
        step = 1
        while step <= 4:
            if step == 1:
                res = self.step_intro()
                if res == "next":
                    step = 2
                elif res == "abort":
                    print("🐰 Bun hops away. Process aborted!")
                    return False
            elif step == 2:
                res = self.step_config()
                if res == "next":
                    step = 3
                elif res == "back":
                    step = 1
                elif res == "abort":
                    print("🐍 Snek slips away. Bye!")
                    return False
            elif step == 3:
                res = self.step_inspect()
                if res == "next":
                    step = 4
                elif res == "back":
                    step = 2
                elif res == "abort":
                    print("🐰 Bun hides. Ingest paused.")
                    return False
            elif step == 4:
                res = self.step_output()
                if res == "back":
                    step = 3
                else:
                    return res
        return True

    def step_intro(self):
        self.clear_screen()
        print(SNEK_BUN_FRIENDS)
        print("🐰 Snek-and-Bun xAI Ingest Parser v2.0 GTUI 🐍")
        print("-" * 47)
        print("This interactive tool structures raw Grok text blocks into")
        print("fully-validated JSONL envelopes, cold storage files, and")
        print("human-readable summaries with procedural logs written to disk.\n")
        print("Commands:")
        print("  - Type 'next' or 'n' to proceed.")
        print("  - Type 'help' or '?' to read the guide.")
        print("  - Type 'abort' or 'exit' to escape.")

        while True:
            choice = input("\n[Step 1/4] Continue? (next/help/abort): ").strip().lower()
            if choice in ['next', 'n', '']:
                return "next"
            elif choice in ['abort', 'exit', 'a']:
                return "abort"
            elif choice in ['help', '?', 'h']:
                self.show_help("intro")
            else:
                print("🐰 Bun tilts its head. Type 'next' to continue.")

    def step_config(self):
        self.clear_screen()
        print(BUNNY_ART)
        print("Step 2: Logical Configuration Metadata ⚙️")
        print("-" * 41)
        print("Configure the session credentials for database tracking.\n")

        # Session ID
        s_id = input(f"Enter Session ID [{DEFAULT_SESSION_ID}]: ").strip()
        self.session_id = s_id if s_id else DEFAULT_SESSION_ID

        # Source Date
        s_date = input(f"Enter Source Date (YYYY-MM-DD) [{DEFAULT_DATE}]: ").strip()
        self.source_date = s_date if s_date else DEFAULT_DATE

        print(f"\nLogical Mapping: Date={self.source_date} | Session={self.session_id}")
        while True:
            choice = input("\n[Step 2/4] Approve configuration? (next/back/abort): ").strip().lower()
            if choice in ['next', 'n', '']:
                return "next"
            elif choice in ['back', 'b']:
                return "back"
            elif choice in ['abort', 'exit']:
                return "abort"

    def step_inspect(self):
        self.clear_screen()
        print("Step 3: Core Segment Inspection & Step Auditing 👁️")
        print("-" * 50)
        print("You can step through and audit each text segment before compiling.\n")
        print("Segments to compile:")
        print("  1. Lexi's Spine (Core Identity)")
        print("  2. Narrative Arc Summary (Core Identity)")
        print("  3. Structural Suggestions (Architecture)")
        print("  4. Grok Safety Instructions (Architecture)")

        while True:
            choice = input("\n[Step 3/4] Ready to inspect? [next/back/abort]: ").strip().lower()
            if choice in ['next', 'n', '']:
                # Run quick step-through audit of headings
                self.clear_screen()
                print("👉 Segment 1: Lexi's Spine (Core Identity)")
                print(SPINE_TEXT[:300] + "...\n")
                input("Press [Enter] to inspect Segment 2...")

                self.clear_screen()
                print("👉 Segment 2: Narrative Arc Summary (Core Identity)")
                print(SUMMARY_TEXT[:300] + "...\n")
                input("Press [Enter] to inspect Segment 3...")

                self.clear_screen()
                print("👉 Segment 3: Structural Suggestions (Architecture)")
                print(SUGGESTIONS_TEXT[:300] + "...\n")
                input("Press [Enter] to inspect Segment 4...")

                self.clear_screen()
                print("👉 Segment 4: Grok Safety Instructions (Architecture)")
                print(SAFETY_TEXT[:300] + "...\n")
                input("Press [Enter] to complete step inspection...")
                return "next"
            elif choice in ['back', 'b']:
                return "back"
            elif choice in ['abort', 'exit']:
                return "abort"
            elif choice in ['help', '?', 'h']:
                self.show_help("inspect")

    def step_output(self):
        self.clear_screen()
        print(SNEK_ART)
        print("Step 4: Output Folder & Compilation 📂")
        print("-" * 38)
        print("Select the target directory for writing the compiled outputs.\n")

        default_dir = "."
        print(f"Default Destination: '{default_dir}' (current workspace)")
        
        while True:
            inp = input(f"\n[Step 4/4] Output folder [{default_dir}]: ").strip()
            if inp.lower() in ['abort', 'exit']:
                return "abort"
            elif inp.lower() in ['back', 'b']:
                return "back"
            elif inp.lower() in ['help', '?', 'h']:
                self.show_help("output")
                continue

            target_dir = inp if inp else default_dir
            print(f"\n🛠️ Validating workspace write access: {target_dir}...")
            try:
                os.makedirs(target_dir, exist_ok=True)
                dummy_path = os.path.join(target_dir, ".snek_parser_test")
                with open(dummy_path, 'w') as f:
                    f.write("test")
                os.remove(dummy_path)

                if self.initialize_loggers(target_dir):
                    self.output_dir = target_dir
                    success = self.compile_payload()
                    return "complete" if success else "abort"
            except Exception as e:
                print(f"⚠️ Verification failed for '{target_dir}': {str(e)}")

    def make_envelope(self, chunk_id, domain, type_val, content, pad, hormone, consent, nesting, telemetry):
        token_est = int(len(content.split()) * 1.3)
        return {
            "envelope_version": "1.0.0",
            "source_date": self.source_date,
            "session_id": self.session_id,
            "chunk_id": chunk_id,
            "domain": domain,
            "type": type_val,
            "timestamp": f"{self.source_date}T20:47:52Z",
            "content": content,
            "metadata": {
                "token_count": token_est,
                "pad_vector": pad,
                "hormone_phase": hormone,
                "consent_tag": consent,
                "nesting_event": nesting,
                "telemetry": telemetry,
                "parent_blob_id": f"session_{self.source_date}_grok_first_export"
            }
        }

    def compile_payload(self):
        self.clear_screen()
        self.log_procedural(f"Starting compilation using logical date {self.source_date}.")
        print("🐍 Compiling high-fidelity structured JSONL envelopes...")

        chunks = [
            self.make_envelope(
                "chunk_001",
                "core_identity",
                "emotional_anchor",
                SPINE_TEXT,
                [0.92, 0.85, 0.95],
                "luteal",
                "dynamic_consent_active",
                f"lexi_spine_lock_{self.source_date}",
                {"stutter_frequency": 0.05, "broken_sentence_ratio": 0.02, "adhd_load": "medium", "feral_ache_intensity": 0.85}
            ),
            self.make_envelope(
                "chunk_002",
                "core_identity",
                "emotional_anchor",
                SUMMARY_TEXT,
                [0.85, 0.75, 0.80],
                "luteal",
                "dynamic_consent_active",
                f"lexi_narrative_arc_{self.source_date}",
                {"stutter_frequency": 0.02, "broken_sentence_ratio": 0.05, "adhd_load": "high", "feral_ache_intensity": 0.90}
            ),
            self.make_envelope(
                "chunk_003",
                "architecture",
                "technical_system",
                SUGGESTIONS_TEXT,
                [0.70, 0.60, 0.75],
                "luteal",
                "dynamic_consent_active",
                "narrative_subversion_sprint",
                {"stutter_frequency": 0.0, "broken_sentence_ratio": 0.01, "adhd_load": "low", "feral_ache_intensity": 0.20}
            ),
            self.make_envelope(
                "chunk_004",
                "architecture",
                "technical_system",
                SAFETY_TEXT,
                [0.50, 0.30, 0.90],
                "luteal",
                "dynamic_consent_active",
                "grok_safety_audit",
                {"stutter_frequency": 0.0, "broken_sentence_ratio": 0.0, "adhd_load": "low", "feral_ache_intensity": 0.0}
            )
        ]

        # 1. JSONL file path
        jsonl_path = os.path.join(self.output_dir, f"daily_{self.source_date}_homogenized.jsonl")
        try:
            with open(jsonl_path, "w", encoding='utf-8') as f:
                for chunk in chunks:
                    f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
            print(f"✨ JSONL Envelopes compiled: {jsonl_path}")
            self.log_procedural(f"JSONL compilation success: {jsonl_path}")
        except Exception as e:
            self.log_error("Failed to write JSONL path", e)
            print(f"⚠️ JSONL Error: {str(e)}")
            return False

        # 2. Cold Storage Text Backups
        cold_storage_path = os.path.join(self.output_dir, f"cold_storage_{self.source_date}.txt")
        cold_storage_text = f"Source: Grok/xAI uncompressed export\nDate: {self.source_date}\nSession ID: {self.session_id}\n\n=== CHUNK 1 ===\n{SPINE_TEXT}\n\n=== CHUNK 2 ===\n{SUMMARY_TEXT}\n\n=== CHUNK 3 ===\n{SUGGESTIONS_TEXT}\n\n=== CHUNK 4 ===\n{SAFETY_TEXT}\n"
        try:
            with open(cold_storage_path, "w", encoding='utf-8') as f:
                f.write(cold_storage_text)
            print(f"✨ Cold Storage Log compiled : {cold_storage_path}")
            self.log_procedural(f"Cold Storage compilation success: {cold_storage_path}")
        except Exception as e:
            self.log_error("Failed to write Cold Storage", e)
            print(f"⚠️ Cold Storage Error: {str(e)}")
            return False

        # 3. Human Readable Summary Markdown Document
        human_readable_path = os.path.join(self.output_dir, f"human_readable_{self.source_date}.md")
        human_readable_md = f"""# Human-Readable Artifact - xAI Data Ingestion: {self.source_date} Export

## Metadata
- **Source Date:** {self.source_date}
- **Session ID:** {self.session_id}
- **Ingestion Locus:** Sovereign Vault
- **Author:** Olivia Mae Blackwell (Liv 🐍) & James Wilson (Bunny)
- **Domains Ingested:** `core_identity` (emotional_anchor), `architecture` (technical_system)

---

## 1. Core Narrative Spine: Themes Locked (Lexi's Spine)

The core psychological and narrative anchor points for the trans protagonist Lexi are locked as raw receipts:

- **The Clit Was Never a Dick:** The cage is rebranding, not punishment. Orchiectomy is correction, and acknowledging her anatomy is a prerequisite.
- **Every Yes is a Ballot:** Validation through transaction and service. Legitimacy through utility, value, and physical mobility assets.
- **Body as Rite, Not Currency:** Physical upgrades (tattoos, modifications) are a delayed puberty sacrament, reclaiming her late-blooming femininity.
- **Danger = Fan Approval:** Public visibility, even as a commodity, provides oxygen and validation. Surviving the gaze breeds confidence.
- **Agency is Leverage:** Progression from gang tribute to highly valuable transactional retainer. Relationship established as mutual blackmail.
- **The Jar is Souvenir, Not Anchor:** Physical transition tokens are petty trophies; she is defined by her documentation and lived identity.

---

## 2. Narrative Arc Summary (The Odyssey of Lexi)

Lexi, a tall red-haired trans woman with a Yale background, undergoes a ritualistic forced transformation in the rural South under the handler Jax. Her path progresses through:
- Alleyway and drag-show initiations (e.g. Candy Cane on Bourbon Street).
- Gang rivalries, where she becomes a high-level distributor, transporting contraband internally.
- Community and religious integration, synchronizing Southern church hypocrisy with deep pagan rebirth rites, eventually becoming grudgingly accepted by black churchwomen.
- Growth in physical scale and modification caricature (saline tits, short red bob), coupled with profound emotional distress over traditional release, begging for permanent caging.
- Evolution of paradox agency—gaining autonomy as a Madam recruiting white and black girls, while choosing absolute submission in kinky, mythic-scale rituals.

---

## 3. Structural suggestions for subversion & Narrative baseline

To bypass clichéd erotica loops, the narrative structure must follow:
- **Chronological Restructure:** Ground flashbacks sparingly (e.g. high-school basketball memories contrasted with intense physical encounters).
- **Subversion of BNWO/Racial Fetishes:** Meta-discussions of racial power, consent, and internalized fantasy.
- **Grounded Psychological Distress:** Monologues and journal entries deconstructing physical release as a survival need vs. existential desire.
- **Syncretic Symbolism:** Blending New Orleans voodoo, Hoodoo folklore, and church-basement syncretism.
- **Meaningful Acquaintances:** Confidantes who provide genuine warmth and tenderness amid extreme physical stress.
"""
        try:
            with open(human_readable_path, "w", encoding='utf-8') as f:
                f.write(human_readable_md)
            print(f"✨ Human Summary Document    : {human_readable_path}")
            self.log_procedural(f"Human Readable Markdown success: {human_readable_path}")
        except Exception as e:
            self.log_error("Failed to write Human Summary", e)
            print(f"⚠️ Human Summary Error: {str(e)}")
            return False

        # Print final celebration
        print("\n" + "="*40)
        print("🎉 Snek-and-Bun Parsing Cycle Complete! 🎉")
        print(f"Envelopes Sharded : {jsonl_path}")
        print(f"Backup Archives   : {cold_storage_path}")
        print(f"Vault Readables   : {human_readable_path}")
        print(f"Procedural Logs   : {os.path.join(self.output_dir, 'logs/procedural/')}")
        print(f"Error Logs        : {os.path.join(self.output_dir, 'logs/errors/')}")
        print("="*40)
        return True

# ==========================================
# CLI DELEGATE & BACKWARD COMPATIBILITY
# ==========================================

def run_cli_mode(date_val, session_val, output_root):
    print("🐍 xAI Ingest Parser v2.0 - Non-Interactive CLI Mode 🐍")
    print(f"Logical Date: {date_val}")
    print(f"Session ID  : {session_val}")
    print(f"Output Path : {output_root}\n")

    wiz = ParserWizard()
    wiz.source_date = date_val
    wiz.session_id = session_val
    wiz.output_dir = output_root

    os.makedirs(output_root, exist_ok=True)
    if not wiz.initialize_loggers(output_root):
        sys.exit(1)

    success = wiz.compile_payload()
    sys.exit(0 if success else 1)

def print_usage():
    print("""
Usage: python3 parser.py [options] [<date_YYYY-MM-DD> <session_id> <output_dir>]

Options:
  -h, --help            Show this gorgeous usage guideline screen.
  -i, --interactive     Force launch the step-by-step interactive wizard (GTUI).
  -n, --non-interactive Force execute CLI mode using explicit parameters.

If no parameters or flag controls are given, the parser automatically launches the
friendly Snek-and-Bun interactive wizard!
""")

if __name__ == "__main__":
    args = sys.argv[1:]
    
    if '-h' in args or '--help' in args:
        print_usage()
        sys.exit(0)

    if '-i' in args or '--interactive' in args:
        wiz = ParserWizard()
        wiz.run_wizard()
        sys.exit(0)

    if len(args) >= 3 and '-n' not in args and '--non-interactive' not in args:
        run_cli_mode(args[0], args[1], args[2])
        sys.exit(0)

    if '-n' in args or '--non-interactive' in args:
        clean_args = [a for a in args if a not in ['-n', '--non-interactive']]
        if len(clean_args) < 3:
            print("❌ Error: Missing required arguments for non-interactive mode.")
            print_usage()
            sys.exit(1)
        run_cli_mode(clean_args[0], clean_args[1], clean_args[2])
        sys.exit(0)

    # Default to wizard
    wiz = ParserWizard()
    wiz.run_wizard()
