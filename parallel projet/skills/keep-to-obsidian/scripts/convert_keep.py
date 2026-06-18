import os
import json
import re
from datetime import datetime

def sanitize_filename(name):
    # Remove illegal characters for Unix and Windows filesystems
    name = re.sub(r'[\\/*?:"<>|]', '', name)
    # Remove trailing/leading spaces
    name = name.strip()
    # Limit length to avoid long path issues
    return name[:100] if name else "Untitled"

def convert_timestamp(usec_epoch):
    if not usec_epoch:
        return ""
    try:
        # Microseconds to seconds
        dt = datetime.fromtimestamp(usec_epoch / 1000000.0)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return ""

def clean_tag(label_name):
    # Convert labels to Obsidian tags (only alphanumeric, hyphens, and slashes allowed in tags usually)
    # Replace spaces with hyphens
    tag = label_name.replace(" ", "-")
    # Remove characters that aren't letters, numbers, hyphens, or underscores
    tag = re.sub(r'[^a-zA-Z0-9_\-/]', '', tag)
    return tag.lower()

def convert_note_to_markdown(json_data):
    title = json_data.get("title", "").strip()
    text_content = json_data.get("textContent", "").strip()
    list_content = json_data.get("listContent", [])
    
    # Resolve blank title
    if not title:
        if text_content:
            # Use first 30 characters of body
            first_line = text_content.split("\n")[0].strip()
            title = first_line[:30] if len(first_line) > 0 else "Untitled"
        elif list_content:
            # Use first list item text
            first_item = list_content[0].get("text", "Untitled").strip()
            title = f"Checklist - {first_item[:30]}"
        else:
            title = "Untitled"

    # Sanitize title for file name
    safe_title = sanitize_filename(title)
    
    # Process Timestamps
    created_time = convert_timestamp(json_data.get("createdTimestampUsec"))
    edited_time = convert_timestamp(json_data.get("userEditedTimestampUsec"))
    
    # Process Tags
    labels = json_data.get("labels", [])
    tags = [clean_tag(l.get("name")) for l in labels if l.get("name")]
    
    # Process Flags
    is_archived = json_data.get("isArchived", False)
    is_pinned = json_data.get("isPinned", False)
    color = json_data.get("color", "DEFAULT")

    # Build Frontmatter
    frontmatter = [
        "---",
        f"title: \"{title}\"",
        f"created: \"{created_time}\"" if created_time else "created:",
        f"modified: \"{edited_time}\"" if edited_time else "modified:",
        "tags:"
    ]
    if tags:
        for tag in tags:
            frontmatter.append(f"  - {tag}")
    else:
        frontmatter.append("  - keep-import")
        
    frontmatter.extend([
        f"archived: {str(is_archived).lower()}",
        f"pinned: {str(is_pinned).lower()}",
        f"color: {color}",
        "---\n"
    ])
    
    # Build Note Body
    body_lines = []
    
    # Standard Text Note
    if text_content:
        body_lines.append(text_content)
        
    # Checklist Note
    if list_content:
        if text_content:
            body_lines.append("\n---")  # Separator if both exist
        for item in list_content:
            text = item.get("text", "").strip()
            is_checked = item.get("isChecked", False)
            checkbox = "x" if is_checked else " "
            body_lines.append(f"- [{checkbox}] {text}")
            
    markdown_content = "\n".join(frontmatter) + "\n".join(body_lines)
    return safe_title, markdown_content

def process_keep_export(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    archive_dir = os.path.join(output_dir, "Archive")
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    processed_count = 0
    skipped_count = 0

    for filename in os.listdir(input_dir):
        if not filename.endswith(".json"):
            continue
            
        file_path = os.path.join(input_dir, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Skip trashed notes
            if data.get("isTrashed", False):
                skipped_count += 1
                continue
                
            safe_title, md_content = convert_note_to_markdown(data)
            
            # Determine path (save archived notes in an Archive subfolder)
            is_archived = data.get("isArchived", False)
            target_folder = archive_dir if is_archived else output_dir
            
            # Prevent file overwrite by appending a suffix if file exists
            output_file_name = f"{safe_title}.md"
            output_file_path = os.path.join(target_folder, output_file_name)
            
            counter = 1
            while os.path.exists(output_file_path):
                output_file_name = f"{safe_title} ({counter}).md"
                output_file_path = os.path.join(target_folder, output_file_name)
                counter += 1
                
            with open(output_file_path, "w", encoding="utf-8") as out_f:
                out_f.write(md_content)
                
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print(f"\nProcessing Complete!")
    print(f"Processed: {processed_count} notes successfully.")
    print(f"Skipped: {skipped_count} trashed notes.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert Google Keep Takeout JSON files to Markdown.")
    parser.add_argument("input_dir", help="Directory containing the extracted Google Keep JSON files.")
    parser.add_argument("output_dir", help="Directory where converted Markdown files should be saved.")
    args = parser.parse_args()
    process_keep_export(args.input_dir, args.output_dir)
