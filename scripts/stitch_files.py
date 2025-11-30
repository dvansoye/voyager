import argparse
import os
import sys
from dotenv import load_dotenv

def find_file_in_vault(filename, vault_root):
    search_paths = [
        vault_root,
        os.path.join(vault_root, "Zettelkasten"),
        os.path.join(vault_root, "Zettelkasten", "Zettele"),
        os.path.join(vault_root, "Zettelkasten", "Tagebuch"),
        os.path.join(vault_root, "Zettelkasten", "Git-Obsidian", "status-reports")
    ]

    target_path = None
    for folder in search_paths:
        candidate = os.path.join(folder, filename)
        if os.path.exists(candidate):
            target_path = candidate
            break
    
    if not target_path:
        for root, dirs, files in os.walk(vault_root):
            if '.git' in dirs:
                dirs.remove('.git')
                
            if filename in files:
                target_path = os.path.join(root, filename)
                break
    return target_path

def main():
    load_dotenv()
    # Retrieve the Vault Path
    vault_root = os.getenv('OBSIDIAN_VAULT_PATH')
    
    if not vault_root:
        sys.stderr.buffer.write("Error: OBSIDIAN_VAULT_PATH environment variable not set.\n".encode('utf-8'))
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Stitch multiple files from the Obsidian Vault into a single output file.")
    parser.add_argument('inputs', nargs='+', help='List of input file paths (relative to Vault).')
    parser.add_argument('--output', required=True, help='Path for the merged output file.')
    parser.add_argument('--header-file', help='Optional path to a markdown file (template) to prepend to the output.')

    args = parser.parse_args()

    try:
        with open(args.output, 'w', encoding='utf-8') as outfile:
            # --- HEADER PROCESSING ---
            if args.header_file:
                # We still check locally for the template since it lives in the Voyager repo
                if not os.path.exists(args.header_file):
                    sys.stderr.buffer.write(f"Warning: Header file '{args.header_file}' not found. Skipping.\n".encode('utf-8'))
                else:
                    with open(args.header_file, 'r', encoding='utf-8') as header_file:
                        outfile.write(header_file.read())
                        outfile.write("\n\n")

            # --- BODY PROCESSING (Strictly Vault) ---
            for input_filename in args.inputs:
                target_file_path = find_file_in_vault(input_filename, vault_root)

                if not target_file_path:
                    sys.stderr.buffer.write(f"Warning: File '{input_filename}' not found in Vault. Skipping.\n".encode('utf-8'))
                    continue
                
                try:
                    with open(target_file_path, 'r', encoding='utf-8') as infile:
                        file_content = infile.read()
                        
                    if file_content:
                        outfile.write(f"\n--- [{os.path.basename(input_filename)}] ---\n")
                        outfile.write(file_content)
                        outfile.write("\n") # Ensure a newline after each file's content
                        
                except Exception as e:
                    sys.stderr.buffer.write(f"Warning: Could not read file '{target_file_path}': {e}. Skipping.\n".encode('utf-8'))
                    continue

    except Exception as e:
        sys.stderr.buffer.write(f"Error: {e}\n".encode('utf-8'))
        sys.exit(1)

if __name__ == "__main__":
    main()