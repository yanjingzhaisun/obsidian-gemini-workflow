import os
import re
import sys
from pathlib import Path

# Add script directories to find TagAnalyzer and ObsidianClient
root_dir = Path(__file__).resolve().parents[4]
sys.path.append(str(root_dir / "scripts"))
sys.path.append(str(root_dir / ".gemini/skills/obsidian-tag-cleanup/scripts"))

from analyze_tags import TagAnalyzer
from obsidian_client import ObsidianClient

class LinkGenerator:
    def __init__(self, vault_path=None):
        self.client = ObsidianClient(vault_path)
        self.vault_root = self.client.vault_path
        self.analyzer = TagAnalyzer(vault_path)

    def is_permanent(self, tags):
        return "status/permanent" in tags

    def is_moc(self, file_name, tags):
        if "MOC" in file_name or "moc" in file_name.lower():
            return True
        # Check if MOC tag exists (case-insensitive check)
        for tag in tags:
            if "moc" in tag.lower():
                return True
        return False

    def run(self):
        """Finds and links unlinked mentions of permanent notes."""
        permanent_notes = {} # {title: path}
        
        # 1. Gather all permanent notes (excluding MOCs)
        for root, _, files in os.walk(self.vault_root):
            if '.obsidian' in root or '.git' in root:
                continue
            for file in files:
                if file.endswith('.md'):
                    full_path = Path(root) / file
                    tags = self.analyzer.extract_tags_from_file(full_path)
                    
                    if self.is_permanent(tags) and not self.is_moc(file, tags):
                        title = file[:-3] # Remove .md
                        # Exclude very short titles to avoid over-linking common words
                        if len(title) > 2:
                            permanent_notes[title] = full_path

        print(f"Found {len(permanent_notes)} permanent non-MOC notes to cross-reference.")

        # 2. Scan and add links
        files_updated = 0
        links_added = 0
        
        # Sort titles by length descending so longer titles are matched first
        # E.g., match "Game Design" before "Game"
        titles_to_match = sorted(permanent_notes.keys(), key=len, reverse=True)

        for title, target_path in permanent_notes.items():
            try:
                with open(target_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {target_path}: {e}")
                continue

            original_content = content
            
            # Separate frontmatter from body
            frontmatter_match = re.search(r'^---\s*\r?\n.*?\n---\s*(?:\r?\n|$)', content, re.DOTALL)
            if frontmatter_match:
                frontmatter = content[:frontmatter_match.end()]
                body = content[frontmatter_match.end():]
            else:
                frontmatter = ""
                body = content
            
            # Find references to OTHER permanent notes in the body
            for other_title in titles_to_match:
                if title == other_title:
                    continue # Don't link to itself
                
                escaped_title = re.escape(other_title)
                pattern = rf'(?<!\[\[)(?<!\[){escaped_title}(?!\]\])(?!\])'
                
                try:
                    body, num_subs = re.subn(pattern, rf'[[{other_title}]]', body)
                    if num_subs > 0:
                        links_added += num_subs
                except Exception as e:
                    print(f"Regex error on title '{other_title}': {e}")

            content = frontmatter + body
            if content != original_content:
                try:
                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Added links to: {target_path.relative_to(self.vault_root)}")
                    files_updated += 1
                except Exception as e:
                    print(f"Error writing {target_path}: {e}")

        print(f"\n--- Summary ---")
        print(f"Files updated: {files_updated}")
        print(f"Total new links added: {links_added}")

if __name__ == "__main__":
    generator = LinkGenerator()
    generator.run()
