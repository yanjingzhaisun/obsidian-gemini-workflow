import os
import yaml
import re
from pathlib import Path

def extract_frontmatter(content):
    """Extracts frontmatter from markdown content."""
    # Matches --- (any content) --- at the start of the file
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        return match.group(1), content[match.end():]
    return None, content

def update_daily_note_frontmatter(file_path):
    """Updates the frontmatter of a single daily note."""
    file_path = Path(file_path)
    # Extract date from filename (YYYY-MM-DD.md)
    date_match = re.match(r'^(\d{4}-\d{2}-\d{2})\.md$', file_path.name)
    if not date_match:
        print(f"Skipping {file_path.name}: Filename does not match YYYY-MM-DD.md")
        return False
    
    file_date = date_match.group(1)
    target_date_str = f"{file_date}T00:00"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        fm_raw, body = extract_frontmatter(content)
        
        if fm_raw:
            try:
                fm = yaml.safe_load(fm_raw) or {}
            except yaml.YAMLError as e:
                print(f"Error parsing YAML in {file_path.name}: {e}")
                return False
        else:
            fm = {}
        
        # Update or add tags
        if 'tags' not in fm:
            fm['tags'] = []
        elif not isinstance(fm['tags'], list):
            # If tags is a string, convert to list
            fm['tags'] = [fm['tags']]
        
        # Ensure status/permanent and daily are in tags
        required_tags = ['status/permanent', 'daily']
        for tag in required_tags:
            if tag not in fm['tags']:
                fm['tags'].append(tag)
        
        # Update or add date
        fm['date'] = target_date_str
        
        # Re-serialize frontmatter
        # Dumper=yaml.SafeDumper and default_flow_style=False ensures list format
        new_fm_raw = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False, indent=2)
        
        new_content = f"---\n{new_fm_raw}---\n{body}"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Updated {file_path.name}")
        return True
        
    except Exception as e:
        print(f"Unexpected error processing {file_path.name}: {str(e)}")
        return False

def run_fix():
    # Using the path provided by the user
    daily_notes_dir = Path("/home/zed/Documents/default_vault/daily_notes/")
    
    if not daily_notes_dir.exists():
        print(f"Directory not found: {daily_notes_dir}")
        return
    
    md_files = list(daily_notes_dir.glob("*.md"))
    
    print(f"Processing {len(md_files)} files in {daily_notes_dir}...")
    
    updated_count = 0
    for md_file in md_files:
        if update_daily_note_frontmatter(md_file):
            updated_count += 1
            
    print(f"\nSuccessfully updated {updated_count} files.")

if __name__ == "__main__":
    run_fix()
