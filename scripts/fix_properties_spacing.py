import os
import re
from pathlib import Path

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Matches the second --- if it's immediately followed by a character (not a newline/space)
    # The first --- is at the start of the file.
    # We look for a pattern where frontmatter ends and text starts on the same line.
    
    # Regex: Start of file, then content, then --- then NON-WHITESPACE
    # We use a more robust regex that specifically targets the frontmatter closure.
    pattern = r'^(---\s*\n.*?\n---)([^\s\n\-])'
    
    new_content, count = re.subn(pattern, r'\1\n\2', content, flags=re.DOTALL)
    
    if count > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

if __name__ == "__main__":
    vault_path = r"C:\Users\zhouzijian\Documents\main-vault"
    modified_count = 0
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith('.md'):
                full_path = Path(root) / file
                if fix_file(full_path):
                    print(f"Fixed: {full_path.relative_to(vault_path)}")
                    modified_count += 1
    print(f"Total files fixed: {modified_count}")
