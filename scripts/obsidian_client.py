import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class ObsidianClient:
    def __init__(self, vault_path=None):
        self.vault_path = vault_path or os.getenv("OBSIDIAN_VAULT_PATH")
        if not self.vault_path:
            raise ValueError("OBSIDIAN_VAULT_PATH is not set in .env or provided.")
        
        self.vault_path = Path(self.vault_path).resolve()
        if not self.vault_path.exists():
            raise FileNotFoundError(f"Vault path does not exist: {self.vault_path}")

    def _run_command(self, *args):
        """Helper to run obsidian CLI commands."""
        # The official CLI often uses 'obsidian' as the command.
        # We might need to handle cases where it's not in the PATH.
        try:
            cmd = ["obsidian", "--vault", str(self.vault_path)] + list(args)
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running obsidian command: {e.stderr}")
            raise
        except FileNotFoundError:
            raise RuntimeError("The 'obsidian' command was not found. Please ensure the Obsidian CLI is enabled and in your PATH.")

    def open_note(self, note_path):
        """Opens a specific note in Obsidian."""
        return self._run_command("open", note_path)

    def list_files(self):
        """Lists files in the vault using the CLI (if supported) or filesystem."""
        # If the CLI doesn't support 'list', we can fallback to filesystem.
        # But for Phase 2, we want to wrap the CLI where possible.
        # Let's assume 'ls' or similar might exist in future or we use filesystem for now.
        return [str(p.relative_to(self.vault_path)) for p in self.vault_path.glob("**/*.md")]

if __name__ == "__main__":
    client = ObsidianClient()
    print(f"Vault Path: {client.vault_path}")
    # Example usage:
    # client.open_note("inbox/test.md")
