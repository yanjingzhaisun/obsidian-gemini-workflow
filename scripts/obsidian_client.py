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
        
        # Strip potential extra quotes from the environment variable value
        self.vault_path = self.vault_path.strip('"').strip("'")
        
        self.vault_path = Path(self.vault_path).resolve()
        if not self.vault_path.exists():
            raise FileNotFoundError(f"Vault path does not exist: {self.vault_path}")

    def _run_command(self, command, **kwargs):
        """Helper to run obsidian CLI commands with arguments."""
        try:
            # Base command
            cmd = ["obsidian", command, f"vault={self.vault_path.name}"]
            
            # Add arguments
            for key, value in kwargs.items():
                if value is True:
                    cmd.append(key)
                elif value is not False and value is not None:
                    cmd.append(f"{key}={value}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # Check if the error is due to Obsidian not being open
            error_msg = e.stderr.lower()
            if "could not connect" in error_msg or "not running" in error_msg or not e.stderr:
                raise RuntimeError(
                    "Error: Could not connect to Obsidian. \n"
                    "IMPORTANT: The Obsidian application must be open and the 'Obsidian CLI' plugin must be active for these commands to work."
                )
            print(f"Error running obsidian {command}: {e.stderr}")
            raise
        except FileNotFoundError:
            raise RuntimeError("The 'obsidian' command was not found. Please ensure the Obsidian CLI is enabled and in your PATH.")

    def read_note(self, path):
        """Reads note content using the official CLI."""
        return self._run_command("read", path=path)

    def write_property(self, path, name, value):
        """Sets a property on a file."""
        return self._run_command("property:set", path=path, name=name, value=value)

    def get_tags(self, path=None):
        """Lists tags, optionally for a specific file."""
        kwargs = {"path": path} if path else {}
        return self._run_command("tags", **kwargs)

    def search(self, query):
        """Searches the vault."""
        return self._run_command("search", query=query)

    def list_files(self, folder=None):
        """Lists files using the official CLI."""
        kwargs = {"folder": folder} if folder else {}
        output = self._run_command("files", **kwargs)
        return output.splitlines()

if __name__ == "__main__":
    client = ObsidianClient()
    print(f"Vault Path: {client.vault_path}")
    # Example usage:
    # client.open_note("inbox/test.md")
