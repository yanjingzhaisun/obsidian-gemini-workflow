import os
import re
from pathlib import Path
from obsidian_client import ObsidianClient

class TagCleaner:
    def __init__(self, vault_path=None):
        self.client = ObsidianClient(vault_path)
        self.vault_root = self.client.vault_path
        
        # Define replacement map: {old_tag: new_tag}
        # Supports regex-like logic for hierarchical roots
        self.replacements = {
            r'audio/engineering': 'music/production',
            r'music/production': 'music/production', # Keep as is
            r'game-design': 'game/design',
            r'game-dev': 'game/dev',
            # Add specific sub-tags if they don't follow simple root replacement
        }

    def clean_content(self, content):
        """Replaces tags in YAML and inline."""
        modified = False
        
        # 1. Process YAML tags
        def yaml_replacer(match):
            nonlocal modified
            inner = match.group(1)
            new_inner = inner
            
            # Simple root replacements for YAML list items
            # Example: - game-design/theory -> - game/design/theory
            patterns = [
                (r'-\s+game-design', '- game/design'),
                (r'-\s+game-dev', '- game/dev'),
                (r'-\s+audio/engineering', '- music/production'),
            ]
            
            for old, new in patterns:
                if re.search(old, new_inner):
                    new_inner = re.sub(old, new, new_inner)
                    modified = True
            return f"---\n{new_inner}\n---"

        content = re.sub(r'^---\s*\n(.*?)\n---\s*\n', yaml_replacer, content, flags=re.DOTALL)

        # 2. Process Inline Tags (#tag)
        # Avoid matching hex, etc.
        def inline_replacer(match):
            nonlocal modified
            full_match = match.group(0) # #game-design/theory
            tag_name = match.group(1)   # game-design/theory
            
            new_tag = tag_name
            if tag_name.startswith('game-design'):
                new_tag = tag_name.replace('game-design', 'game/design', 1)
            elif tag_name.startswith('game-dev'):
                new_tag = tag_name.replace('game-dev', 'game/dev', 1)
            elif tag_name.startswith('audio/engineering'):
                new_tag = tag_name.replace('audio/engineering', 'music/production', 1)
            
            if new_tag != tag_name:
                modified = True
                return f"#{new_tag}"
            return full_match

        content = re.sub(r'(?<!\w)#([a-zA-Z\u4e00-\u9fa5][\w\-/]*)', inline_replacer, content)
        
        return content, modified

    def run(self):
        """Iterate over all files and apply cleaning."""
        count = 0
        for root, _, files in os.walk(self.vault_root):
            if '.obsidian' in root or '.git' in root:
                continue
            for file in files:
                if file.endswith('.md'):
                    path = Path(root) / file
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content, was_modified = self.clean_content(content)
                    
                    if was_modified:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated: {path.relative_to(self.vault_root)}")
                        count += 1
        print(f"Total files updated: {count}")

if __name__ == "__main__":
    cleaner = TagCleaner()
    cleaner.run()
