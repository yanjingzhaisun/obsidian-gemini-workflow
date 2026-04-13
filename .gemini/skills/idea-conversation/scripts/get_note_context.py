import os
import re
import sys
from pathlib import Path

# Add root scripts to sys.path to find obsidian_client
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))

from obsidian_client import ObsidianClient

class NoteContextFetcher:
    def __init__(self, vault_path=None):
        self.client = ObsidianClient(vault_path)
        self.vault_root = self.client.vault_path

    def get_backlinks(self, note_title):
        """Finds files that link to the given note title using the vault search."""
        # We search for [[note_title]] or [[note_title|alias]]
        query = f"[[{note_title}"
        results = self.client.search(query)
        
        # Parse the output which is typically a list of paths
        backlinks = []
        if results:
            for line in results.splitlines():
                if line.strip().endswith('.md'):
                    backlinks.append(line.strip())
        return list(set(backlinks))

    def get_context(self, relative_path):
        """Returns content, tags, and backlinks for a note."""
        try:
            content = self.client.read_note(relative_path)
            tags = self.client.get_tags(relative_path).splitlines()
            
            note_title = Path(relative_path).stem
            backlinks = self.get_backlinks(note_title)
            
            # Filter out the note itself from backlinks
            backlinks = [b for b in backlinks if b != relative_path]
            
            return {
                "path": relative_path,
                "content": content,
                "tags": tags,
                "backlinks": backlinks
            }
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    import sys
    import json
    if len(sys.argv) < 2:
        print("Usage: python get_note_context.py <relative_path>")
        sys.exit(1)
    
    fetcher = NoteContextFetcher()
    context = fetcher.get_context(sys.argv[1])
    print(json.dumps(context, ensure_ascii=False, indent=2))
