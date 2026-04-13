import os
import re
import sys
from pathlib import Path

# Add root scripts to sys.path to find obsidian_client
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))

from obsidian_client import ObsidianClient

class TagCleaner:
    def __init__(self, vault_path=None):
        self.client = ObsidianClient(vault_path)
        self.vault_root = self.client.vault_path
        
        # Define replacement map: {old_root: new_root}
        # This will match the beginning of a tag
        self.replacements = {
            'audio/engineering': 'music/production',
            'game-design': 'game/design',
            'game-dev': 'game/dev',
            'life-pro-tips': 'life/tips',
            'relationship': 'life/people',
            'lyrics/inspiration': 'music/lyrics',
        }

    def clean_content(self, content):
        """Replaces tags in YAML and inline."""
        modified = False
        
        # 1. Process YAML tags
        def yaml_replacer(match):
            nonlocal modified
            inner = match.group(1)
            new_inner = inner
            
            for old, new in self.replacements.items():
                # Pattern for YAML list items: "- old/subtag" -> "- new/subtag"
                # We use regex to ensure we only match the start of the tag after the dash
                pattern = rf'(-\s+){re.escape(old)}'
                if re.search(pattern, new_inner):
                    new_inner = re.sub(pattern, rf'\1{new}', new_inner)
                    modified = True
            return f"---\n{new_inner}\n---"

        content = re.sub(r'^---\s*\n(.*?)\n---\s*\n', yaml_replacer, content, flags=re.DOTALL)

        # 2. Process Inline Tags (#tag)
        def inline_replacer(match):
            nonlocal modified
            full_match = match.group(0) # #old-tag/sub
            tag_name = match.group(1)   # old-tag/sub
            
            for old, new in self.replacements.items():
                if tag_name == old or tag_name.startswith(old + '/'):
                    new_tag = tag_name.replace(old, new, 1)
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
