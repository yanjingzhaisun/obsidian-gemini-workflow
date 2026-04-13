import os
import shutil
import sys
from pathlib import Path

# Add script directories to find TagAnalyzer and ObsidianClient
root_dir = Path(__file__).resolve().parents[4]
sys.path.append(str(root_dir / "scripts"))
sys.path.append(str(root_dir / ".gemini/skills/obsidian-tag-cleanup/scripts"))

from analyze_tags import TagAnalyzer
from obsidian_client import ObsidianClient

class InboxCleaner:
    def __init__(self, vault_path=None):
        self.client = ObsidianClient(vault_path)
        self.vault_root = self.client.vault_path
        self.analyzer = TagAnalyzer(vault_path)
        self.inbox_path = self.vault_root / "inbox"
        self.zettel_path = self.vault_root / "zettlekasten"

    def run(self):
        """Finds permanent notes in inbox and moves them to zettlekasten."""
        if not self.inbox_path.exists():
            print("Inbox folder not found.")
            return

        moved_count = 0
        for root, _, files in os.walk(self.inbox_path):
            for file in files:
                if file.endswith('.md'):
                    full_path = Path(root) / file
                    tags = self.analyzer.extract_tags_from_file(full_path)
                    
                    if "status/permanent" in tags:
                        target_path = self.zettel_path / file
                        
                        # Handle filename collisions
                        if target_path.exists():
                            print(f"Warning: {file} already exists in zettlekasten. Skipping.")
                            continue
                            
                        print(f"Moving: {file} -> zettlekasten/")
                        shutil.move(str(full_path), str(target_path))
                        moved_count += 1
        
        print(f"Total notes moved: {moved_count}")

if __name__ == "__main__":
    cleaner = InboxCleaner()
    cleaner.run()
