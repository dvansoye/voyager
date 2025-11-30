# Mnemosyne Instructions (TXT Handling - Step 1: The Book Summary)

## Objective
You are processing a "TXT" note (a book or long paper). Your goal is to create a new "SUM" (Summary) note, populate it with the first artifact (The Book Summary), and return that summary for the Daily Note.

## Inputs
* **Source File:** The original text file you identified in the main Mnemosyne loop.
* **Template:** `prompts/book_summary_template.md`

## Workflow Sequence

### Step 1: Genesis (Create the Target File)
1.  **Calculate Filename:** You need to derive the new filename.
    * *Logic:* Replace the string "TXT" with "SUM" in the Source Filename.
    * *Tool:* Run this python command to get the string:
        `python -c "print('[Source Filename]'.replace('TXT', 'SUM'))"`
2.  **Read Frontmatter:** Read ONLY the metadata (header) of the Source File.
    * **CRITICAL SAFETY:** Do NOT use `read_note` or `read_file` on the Source File.
    * *Tool:* Run the specific utility script: `python scripts/read_header.py "[Source Filename]"`
3.  **Create File:** Create the new file (the "Target File") in `Zettelkasten/Zettele/`.
    * **CRITICAL TOOLING:** Use the Obsidian MCP tool `Notes`.
    * **Content:** Initialize it with:
        1. The copied YAML frontmatter (lines between `---`) with the following changes:
            * Change `Type: TXT` to `Type: SUM`.
            * Add `Generator: Mnemosyne`.
            * Add `Prompt_Source: prompts/mnemosyneTXT.md`.
            * Add `Model: gemini-2.5-pro`.
            * Add `Run_ID: {{TIMESTAMP}}`.
        2. Two blank lines.
        3. The Cursor Anchor: `# Continue`
        *(This anchor allows us to append future sections without reading the whole file).*

### Step 2: The Book Summary (The Crux)
1.  **Stitch Context:**
    * Combine the Template and the Source File.
    * **Command:** `python scripts/stitch_files.py --output "_temp_summary_context.md" --header-file "prompts/book_summary_template.md" "[Source Filename]"`
2.  **Generate:**
    * Send the huge context to the model.
    * **Command:** `python scripts/call_advanced_model.py --prompt-file "_temp_summary_context.md" --model "gemini-2.5-pro"`
    * *Wait:* This may take a moment.
3.  **Capture & Write (The Cursor Swap)**
    * *Goal:* Use the "Cursor Pattern" to safely add content without reading the large file.
    * **Action A (Write):** Use the Obsidian MCP tool `update_note`.
        * **Method:** Text Replacement (not append).
        * **Target (Old Text):** `# Continue`
        * **Replacement (New Text):**
            ```markdown
            # Book Summary
            [Model Output]

            # Continue
            ```
    * **Action B (Memory):** Store the [Model Output] in your short-term memory as `[Summary]`.

### Step 3: Cleanup & Return
1.  **Delete:** Remove `_temp_summary_context.md`.
2.  **Return:** Output the exact content of `[Summary]`.
    * *Crucial:* Do not wrap it in "Here is the summary". Just output the Markdown content.