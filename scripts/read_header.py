import os
import sys
import io # Import io module
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_frontmatter(filename):
    # 1. Get the Vault Root from .env
    # Check your .env file to ensure the key is named 'OBSIDIAN_VAULT_PATH'
    # Example .env line: OBSIDIAN_VAULT_PATH="C:\Users\Darren\Documents\MyVault"
    vault_root = os.getenv('OBSIDIAN_VAULT_PATH')

    if not vault_root:
        print("[ERROR] OBSIDIAN_VAULT_PATH not found in .env file.")
        print("Please add: OBSIDIAN_VAULT_PATH=/path/to/your/vault")
        sys.exit(1)

    # 2. Define likely locations relative to the Vault Root
    search_paths = [
        vault_root,
        os.path.join(vault_root, "Zettelkasten"),
        os.path.join(vault_root, "Zettelkasten", "Zettele"),
        os.path.join(vault_root, "Zettelkasten", "Tagebuch"),
        os.path.join(vault_root, "Zettelkasten", "Git-Obsidian", "status-reports")
    ]

    target_path = None

    # 3. Fast Search: Check specific folders first
    for folder in search_paths:
        candidate = os.path.join(folder, filename)
        if os.path.exists(candidate):
            target_path = candidate
            break
    
    # 4. Deep Search: Walk the vault if not found in top folders
    if not target_path:
        # print(f"[DEBUG] Searching recursively in {vault_root}...")
        for root, dirs, files in os.walk(vault_root):
            # Optimization: Skip .git or huge hidden folders if necessary
            if '.git' in dirs:
                dirs.remove('.git')
                
            if filename in files:
                target_path = os.path.join(root, filename)
                break

    if not target_path:
        print(f"Error: Could not locate '{filename}' in {vault_root}")
        sys.exit(1)

    # 5. Keyhole Surgery (Read Top 15 Lines)
    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            lines = []
            for _ in range(15):
                line = f.readline()
                if not line: break
                lines.append(line)
        # Print pure output for Roo to capture
        sys.stdout.buffer.write("".join(lines).encode('utf-8'))
    except Exception as e:
        # Explicitly encode error message before writing to stderr
        sys.stderr.buffer.write(f"Error reading file: {e}\n".encode('utf-8'))
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/read_header.py [filename]")
        sys.exit(1)
    
    # Handle cases where Roo passes a full path or just a filename
    filename = os.path.basename(sys.argv[1])
    get_frontmatter(filename)