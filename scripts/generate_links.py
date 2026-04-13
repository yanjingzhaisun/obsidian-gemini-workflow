import os
import re
from pathlib import Path
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
            
            # Find references to OTHER permanent notes
            for other_title in titles_to_match:
                if title == other_title:
                    continue # Don't link to itself
                
                # Regex logic:
                # - Match `other_title` exactly.
                # - Negative lookbehind/lookahead to avoid matching inside existing [[links]]
                # - Using re.escape to handle titles with special regex chars.
                # - This simple regex might not handle all edge cases perfectly (like markdown links [text](url)),
                #   but covers standard plain text well.
                # Note: For Chinese characters, \b might not work as expected at word boundaries.
                # A safer approach for mixed CJK/English is to just check for negative lookbehind `(?<!\[\[)` and lookahead `(?!\]\])`
                
                escaped_title = re.escape(other_title)
                # We want to replace occurrences of the title that are NOT already inside [[ ]]
                # This regex looks for the title, ensuring it's not preceded by [[ or followed by ]]
                # It also tries to avoid matching inside standard markdown links [like this](url) by checking for surrounding brackets, but that's complex.
                # We'll use a simpler heuristic: avoid if inside [[ ]]
                
                # Pattern: Find the title, but only if not surrounded by [[ and ]]
                # This uses a lookaround trick: we match the text if we can't find [[ right before it.
                # Since variable length lookbehinds are not supported in standard python re, we use a simpler approach:
                # Find all occurrences, check context, replace.
                
                # To simplify and ensure safety, we use re.sub with a custom function
                def replacer(match):
                    # We check the entire string to see if the match is inside [[ ]]
                    # A more robust way is to just replace, but Obsidian handles multiple [[[[...]]]] gracefully by showing it weirdly.
                    return f"[[{other_title}]]"
                
                # Pattern to match the title not preceded by [[ and not followed by ]]
                # This is an approximation.
                pattern = rf'(?<!\[\[)(?<!\[){escaped_title}(?!\]\])(?!\])'
                
                try:
                    content, num_subs = re.subn(pattern, rf'[[{other_title}]]', content)
                    if num_subs > 0:
                        links_added += num_subs
                except Exception as e:
                    print(f"Regex error on title '{other_title}': {e}")

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
