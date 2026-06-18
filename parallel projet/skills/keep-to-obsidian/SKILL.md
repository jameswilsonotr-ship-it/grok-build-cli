---
name: keep-to-obsidian
description: Convert Google Keep Takeout JSON files to Obsidian-compatible Markdown files. Use when the user mentions Google Keep, importing Keep notes, converting JSON exports to Markdown, or formatting Keep notes with frontmatter, tags, and checklists.
allowed-tools: vm_shell drive
---

# Keep to Obsidian

A skill that automates the migration of Google Keep Takeout JSON exports into structured, Obsidian-compatible Markdown notes.

## When to Use

- When importing notes from a Google Keep Takeout JSON export.
- When converting Google Keep JSON files to Markdown format.
- When needing notes to be formatted with metadata, proper Obsidian tags, and checklists.

## Steps

1. **Locate the Google Keep Export**: Identify the directory containing the extracted Google Keep JSON files (either locally on the VM or retrieved from Google Drive).

2. **Establish the Output Directory**: Define where the converted Obsidian-compatible Markdown files should be saved.

3. **Execute the Migration Script**: Run the included Python script using `vm_shell`:
   ```bash
   python3 scripts/convert_keep.py <input_dir> <output_dir>
   ```

4. **Verify Converted Notes**:
   - Check that YAML frontmatter contains fields like title, created, modified, tags, archived, pinned, and color.
   - Confirm that checklists are properly formatted with `- [ ]` or `- [x]`.
   - Ensure archived notes are written to an `Archive` subfolder within the output directory.

## Gotchas

- **Trashed Notes**: Trashed notes (notes with `"isTrashed": true` in JSON) are skipped by default.
- **Blank Titles**: If a note has no title, the parser uses the first 30 characters of the body text or first checklist item.
- **Filename Sanitization**: Illegal characters are stripped to prevent filesystem errors.
- **Filename Conflicts**: If multiple notes share the same title, a numerical suffix is added (e.g., "Note (1).md") to avoid overwriting.
