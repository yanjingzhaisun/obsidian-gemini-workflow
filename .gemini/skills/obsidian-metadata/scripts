import os
import yaml
import re
from pathlib import Path
from obsidian_client import ObsidianClient

def extract_frontmatter(content):
    """Extracts frontmatter from markdown content."""
    # Matches --- (any content) --- at the start of the file
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        return match.group(1), content[match.end():]
    return None, content

def validate_frontmatter(file_path):
    """Validates the frontmatter of a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        fm_raw, body = extract_frontmatter(content)
        if not fm_raw:
            return False, ["Missing frontmatter (YAML block) at the top of the file."]
        
        try:
            fm = yaml.safe_load(fm_raw)
        except yaml.YAMLError as e:
            return False, [f"Invalid YAML syntax: {e}"]
        
        errors = []
        
        # 1. Validate tags
        if 'tags' not in fm:
            errors.append("Missing 'tags' field.")
        elif not isinstance(fm['tags'], list):
            errors.append("'tags' must be a list (not a single string).")
        else:
            # Check for status tag
            has_status = any(tag.startswith("status/") for tag in fm['tags'])
            if not has_status:
                errors.append("Missing status tag (e.g., 'status/inbox' or 'status/permanent').")
        
        # 2. Validate date
        if 'date' not in fm:
            errors.append("Missing 'date' field.")
        elif not isinstance(fm['date'], str) or not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}', str(fm['date'])):
            # Handle cases where YAML might parse date as a datetime object
            import datetime
            if isinstance(fm['date'], (datetime.datetime, datetime.date)):
                pass # Accept datetime objects parsed by PyYAML
            else:
                errors.append("'date' must be in ISO 8601 format (YYYY-MM-DDTHH:MM).")
                
        if errors:
            return False, errors
        return True, []
        
    except Exception as e:
        return False, [f"Unexpected error: {str(e)}"]

def run_validation():
    client = ObsidianClient()
    vault_path = client.vault_path
    
    # We'll check all .md files, but we could exclude certain folders like .obsidian/
    md_files = list(vault_path.glob("**/*.md"))
    
    print(f"Scanning {len(md_files)} files in {vault_path}...")
    
    invalid_files = []
    
    for md_file in md_files:
        # Skip files in hidden folders (like .obsidian) or the templates folder
        rel_path = md_file.relative_to(vault_path)
        if any(part.startswith('.') for part in rel_path.parts) or rel_path.parts[0] == 'templates':
            continue
            
        is_valid, errors = validate_frontmatter(md_file)
        if not is_valid:
            invalid_files.append((str(md_file.relative_to(vault_path)), errors))
            
    if invalid_files:
        print(f"\nFound {len(invalid_files)} files with frontmatter issues:\n")
        for file_rel_path, errors in invalid_files:
            print(f"File: {file_rel_path}")
            for err in errors:
                print(f"  - {err}")
    else:
        print("\nAll files follow the frontmatter standard!")

if __name__ == "__main__":
    run_validation()
