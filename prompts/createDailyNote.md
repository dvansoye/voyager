## Objective  
Your objective is to create a daily note if one doesn't already exist.   

## Core Tasks  
Please create a new Daily Note for today.

1. Context & Safety

Target File: Zettelkasten/Tagebuch/{{YYYY-MM-DD}}.md (Use today's date).

Important: Make sure that you are using the Obsidian MCP Server. Do not create the file using the file system. 

Check: Does this file exist? If yes, that's fine. Just return without continuing. 

2. The Template Rendering

Read the template file: Zettelkasten/Vorlagen/Diary.md.

I need you to act as the "Renderer" for this file. Do not copy the code tags; execute their logic:

Dates: Replace <% tp.file.title %> and <% tp.file.creation_date... %> with {{YYYY-MM-DD}}.

Review Date: Replace <% tp.date.now("YYYY-MM-DD", "P1M") %> with the date one month from now.

The Sunday Logic: Locate the block of code starting with <%* let day = ... and ending with <%* } -%>.

IF today is Sunday: Remove the code tags but KEEP the checklist items inside (Backup, DriveSync, etc.).

IF today is NOT Sunday: Remove that entire block (both the code and the checklist items inside it).

3. Execution

Once you have the final text ready, use Notes to save it to the Target File path.