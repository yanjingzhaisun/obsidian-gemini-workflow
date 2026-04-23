import os
import sys
import yaml
from pathlib import Path

def get_vault_path():
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if not vault_path:
        # Fallback for local testing if needed, though Gemini CLI should have it
        return Path("/home/zed/Documents/default_vault")
    return Path(vault_path.strip('"').strip("'"))

def read_md_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {file_path}: {e}"

def collect_inbox_data(inbox_files):
    vault_path = get_vault_path()
    context = "# INBOX DATA\n\n"
    
    for file_name in inbox_files:
        path = vault_path / "inbox" / file_name
        if not path.exists():
            path = vault_path / file_name # try root if not in inbox
        
        if path.exists():
            content = read_md_content(path)
            context += f"## SOURCE: {file_name}\n"
            context += f"PATH: {path}\n"
            context += f"CONTENT:\n{content}\n\n"
        else:
            context += f"## SOURCE: {file_name} (NOT FOUND)\n\n"
            
    return context

def main():
    if len(sys.argv) < 2:
        print("Usage: python collect_context.py <file1.md> <file2.md> ...")
        sys.exit(1)
        
    inbox_files = sys.argv[1:]
    context = collect_inbox_data(inbox_files)
    
    # Print the context for Gemini CLI to consume
    print(context)

if __name__ == "__main__":
    main()
