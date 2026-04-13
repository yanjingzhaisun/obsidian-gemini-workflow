import os
import re
import yaml
from pathlib import Path
from collections import Counter
from obsidian_client import ObsidianClient

class TagAnalyzer:
    def __init__(self, vault_path=None):
        self.client = ObsidianClient(vault_path)
        self.vault_root = self.client.vault_path

    def extract_tags_from_file(self, file_path):
        """Extracts tags from both YAML frontmatter and inline #tags."""
        tags = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. YAML Frontmatter Tags
            frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if frontmatter_match:
                try:
                    data = yaml.safe_load(frontmatter_match.group(1))
                    if data and 'tags' in data:
                        raw_tags = data['tags']
                        if isinstance(raw_tags, list):
                            tags.update(raw_tags)
                        elif isinstance(raw_tags, str):
                            tags.update([t.strip() for t in raw_tags.split(',')])
                except yaml.YAMLError:
                    pass

            # 2. Inline Tags (e.g., #tag/subtag)
            # Regex avoids matching hex codes, URLs, and numeric only tags
            inline_tags = re.findall(r'(?<!\w)#([a-zA-Z\u4e00-\u9fa5][\w\-/]*)', content)
            tags.update(inline_tags)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        
        return tags

    def run(self):
        """Analyzes all markdown files in the vault."""
        tag_counts = Counter()
        file_to_tags = {}

        for root, _, files in os.walk(self.vault_root):
            if '.obsidian' in root or '.git' in root:
                continue
            for file in files:
                if file.endswith('.md'):
                    full_path = Path(root) / file
                    relative_path = full_path.relative_to(self.vault_root)
                    
                    file_tags = self.extract_tags_from_file(full_path)
                    for tag in file_tags:
                        tag_counts[tag] += 1
                    
                    if file_tags:
                        file_to_tags[str(relative_path)] = list(file_tags)

        return tag_counts, file_to_tags

if __name__ == "__main__":
    analyzer = TagAnalyzer()
    counts, file_map = analyzer.run()
    
    print("--- ALL TAGS FOUND ---")
    # Sort tags alphabetically for easier analysis
    for tag in sorted(counts.keys()):
        print(f"{tag} ({counts[tag]})")
