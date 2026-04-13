import os
import re
import yaml
from pathlib import Path
from datetime import datetime

class PropertyAuditor:
    def __init__(self, vault_path=None):
        if vault_path:
            self.vault_root = Path(vault_path)
        else:
            from obsidian_client import ObsidianClient
            self.client = ObsidianClient()
            self.vault_root = self.client.vault_path

    def format_frontmatter(self, data):
        """Formats the data dictionary back into a YAML string."""
        if not data:
            return "---\n---\n"
        
        yaml_str = yaml.dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False)
        return f"---\n{yaml_str}---\n"

    def fix_file(self, file_path, relative_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        modified = False
        original_content = content

        # 1. Fix missing newline after frontmatter
        # We look for a pattern where frontmatter ends and text starts on the same line.
        pattern_spacing = r'^(---\s*\r?\n.*?\n---)([^\s\n\-])'
        content, count = re.subn(pattern_spacing, r'\1\n\2', content, flags=re.DOTALL)
        if count > 0:
            modified = True

        # 2. Parse frontmatter
        frontmatter_match = re.search(r'^---\s*\r?\n(.*?)\n---\s*(?:\r?\n|$)', content, re.DOTALL)
        data = {}
        body = content
        if frontmatter_match:
            frontmatter_text = frontmatter_match.group(1)
            # Fix accidental links in YAML (like date: [[2026-04-13]]) which breaks parsing
            fixed_frontmatter_text, count = re.subn(r'\[\[(.*?)\]\]', r'\1', frontmatter_text)
            if count > 0:
                modified = True
                frontmatter_text = fixed_frontmatter_text
            try:
                data = yaml.safe_load(frontmatter_text) or {}
                body = content[frontmatter_match.end():]
            except yaml.YAMLError as e:
                print(f"Warning: Could not parse YAML in {relative_path}: {e}")
                return False
        else:
            # No frontmatter found, we will create one
            modified = True
            body = content

        if not isinstance(data, dict):
            data = {}
            modified = True

        # 3. Ensure 'tags' is a list
        if 'tags' not in data:
            data['tags'] = []
            modified = True
        elif isinstance(data['tags'], str):
            data['tags'] = [t.strip() for t in data['tags'].split(',')]
            modified = True
        elif not isinstance(data['tags'], list):
            data['tags'] = []
            modified = True

        # 4. Ensure status tag exists
        has_status = any(isinstance(t, str) and t.startswith('status/') for t in data['tags'])
        if not has_status:
            # Determine default status based on folder
            folder_name = Path(relative_path).parts[0] if len(Path(relative_path).parts) > 1 else ""
            if folder_name == "zettlekasten":
                data['tags'].append("status/permanent")
            else:
                data['tags'].append("status/inbox")
            modified = True

        # 5. Ensure 'date' exists
        if 'date' not in data:
            # Use file modification time
            mtime = os.path.getmtime(file_path)
            dt = datetime.fromtimestamp(mtime)
            data['date'] = dt.strftime('%Y-%m-%dT%H:%M')
            modified = True

        # Reconstruct file
        if modified:
            new_frontmatter = self.format_frontmatter(data)
            # Ensure there is exactly one newline between frontmatter and body
            body = body.lstrip()
            new_content = new_frontmatter + body
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True

        return False

    def run(self):
        count = 0
        for root, _, files in os.walk(self.vault_root):
            if '.obsidian' in root or '.git' in root or 'templates' in root:
                continue
            for file in files:
                if file.endswith('.md'):
                    full_path = Path(root) / file
                    relative_path = full_path.relative_to(self.vault_root)
                    
                    try:
                        if self.fix_file(full_path, relative_path):
                            print(f"Fixed properties for: {relative_path}")
                            count += 1
                    except Exception as e:
                        print(f"Error processing {relative_path}: {e}")
                        
        print(f"Total files audited and fixed: {count}")

if __name__ == "__main__":
    auditor = PropertyAuditor()
    auditor.run()
