import argparse
import os
import sys
from dotenv import load_dotenv

def main():
    load_dotenv()
    # Retrieve the Vault Path
    vault_root = os.getenv('OBSIDIAN_VAULT_PATH')
    
    if not vault_root:
        sys.stderr.write("Error: OBSIDIAN_VAULT_PATH environment variable not set.\n")
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
                    sys.stderr.write(f"Warning: Header file '{args.header_file}' not found. Skipping.\n")
                else:
                    with open(args.header_file, 'r', encoding='utf-8') as header_file:
                        outfile.write(header_file.read())
                        outfile.write("\n\n")

            # --- BODY PROCESSING (Strictly Vault) ---
            for input_path in args.inputs:
                
                # 1. Smart Path Cleaning
                # If the Agent passed "Zettelkasten\Tagebuch\...", we want to strip "Zettelkasten\"
                # because it is already in the vault_root.
                vault_name = os.path.basename(vault_root) # e.g., "Zettelkasten"
                clean_input = input_path
                
                # Check if input starts with the vault name
                if input_path.startswith(vault_name + os.sep) or input_path.startswith(vault_name + "/"):
                    # Strip the vault name and separator
                    clean_input = input_path[len(vault_name)+1:]

                # 2. Construct the Absolute Path
                target_file_path = os.path.join(vault_root, clean_input)

                # 3. Read the file
                if not os.path.exists(target_file_path):
                    sys.stderr.write(f"Warning: File '{target_file_path}' not found in Vault. Skipping.\n")
                    continue
                
                try:
                    with open(target_file_path, 'r', encoding='utf-8') as infile:
                        file_content = infile.read()
                        
                    if file_content:
                        outfile.write(f"\n--- [{os.path.basename(input_path)}] ---\n")
                        outfile.write(file_content)
                        outfile.write("\n") # Ensure a newline after each file's content
                        
                except Exception as e:
                    sys.stderr.write(f"Warning: Could not read file '{target_file_path}': {e}. Skipping.\n")
                    continue

    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()