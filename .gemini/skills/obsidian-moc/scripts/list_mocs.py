import os
import sys
from pathlib import Path

# Add root scripts to sys.path to find obsidian_client
root_dir = Path(__file__).resolve().parents[4]
sys.path.append(str(root_dir / "scripts"))

from obsidian_client import ObsidianClient

def list_mocs():
    client = ObsidianClient()
    mocs = []
    
    # 1. Search for MOCs by folder name (if Map-Of-Content exists)
    moc_folder = client.vault_path / "Map-Of-Content"
    if moc_folder.exists() and moc_folder.is_dir():
        for p in moc_folder.glob("*.md"):
            mocs.append(str(p.relative_to(client.vault_path)))
            
    # 2. Search for MOCs by filename pattern across the vault
    # Avoiding duplicates from step 1
    for p in client.vault_path.glob("**/* MOC.md"):
        rel_path = str(p.relative_to(client.vault_path))
        if rel_path not in mocs:
            mocs.append(rel_path)
            
    return mocs

if __name__ == "__main__":
    mocs = list_mocs()
    if mocs:
        print("Found Maps of Content (MOCs):")
        for moc in sorted(mocs):
            print(f"- {moc}")
    else:
        print("No MOCs found.")
