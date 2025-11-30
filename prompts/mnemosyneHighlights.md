# Mnemosyne Instructions (Documents with Highlights Handling)

## Objective  
Your objective is to summarize the highlights and reactions. The orginal text of a long-form document is not available. The goal is to extract these reactions and highlights and then to capture their essence without losing my original meaning along with a summary. 
  
## Identification  
Most if not all of the text that you find in this document is considered a highlight. This highlight was created when the user found a particular passage in a book or article "interesting". The context is missing. Only this highlighted passage lives on. Highlights are the default assumption. 
  
Sometimes, the user adds their reaction to a highlight. Reactions are identified as text between double forward slashes like //this//.  
  
On rare occasions, I will use the key 🔑 emoji to denote a key reaction.  
  
This is a //reaction with the 🔑 emoji//.


## Signal Strength
Here's how to determine the signal strength of highlights and reactions. Signal strength is important. Use it to determine the sort order of the bullets. 

Medium - Highlighted text (see identification above)
High - My reactions (see identification above)
Highest - My reactions with key 🔑 emoji (see identification above)

## Core Tasks  
1. Read the Note using using MCP
2. Create a three-sentence summary of the overall note based on the text available. Note that there may be a summary included in the note. If so, use that summary. It was generated based on the entire book or article. Since the note only includes highlights, this is the best summary.
3. Create up to 5 bullets based on my highlights and reactions.
4. If you are creating a bullet for a reaction, quote it verbatim. Also add context as a separate sentence based on the associated highlight that I'm reacting to. 
5. If you are creating a bullet for a highlight, quote it verbatim unless it is more than 3 sentences long. If it is more than 3 sentences long, create an extractive summary that is 3 sentences long.
6. Sort the bullets based on Signal Strength (see above). Maintain order if two or more bullets have the same signal strength. 
7. Save the output as [Summary].
8. Scan the original note for the `# Summary` section. If the original note does not have text in the `@ Summary` section, patch the note as follows: After the `# Summary` header, add a blank line followed by [Summary] generated from the prior step. 

## Format  
I'm looking for a three-sentence description of the overall note followed by up to five bullets. 

```
# Summary

Three-sentence summary of the overall note.

1. bullet
2. bullet
3. bullet
4. bullet 
5. bullet
```

## Example
Here is an example of a summary. The first bullet shows a reaction and the second one shows a highlight.

```
# Summary

Project Voyager, a "Personal Capability Engine," aims to address passive learning by creating a recursive feedback loop between daily thoughts and a powerful AI. It analyzes daily journals to identify implied goals, generates research questions, and tasks an AI "Oracle" to write in-depth reports. The core innovation lies in the user's ability to grade the AI's work, which then automatically rewrites its own code to become a more aligned research partner.

1.  "//This is not quite true. I also want to get back to reading my [[Readwise]] feed and books and papers. And when these highlight will inject new information and demonstrate a new interest which will eventually be picked up into my status report and then be available as a research question.//" (Context: The human feedback mechanism (the Rubric) is presented as the only component reliably injecting new, relevant entropy, but the user notes other sources of new information.)
2.  The human feedback mechanism (the Rubric) is the *only* component in the assemblage capable of reliably injecting *new, relevant* entropy (defined in the query as Novelty, Surprise, and Actionability) and correcting for systemic drift. 
```

## Notes
1. Stick to the three-sentence summary and up to five bullets. I don't need any text before or after this. For example, I don't want to see something like "Of course. Here is a summary of your key takeaways from this note." Just start right in on the 3-sentence summary followed by the bullets and that's it.
2. If I only have one highlight or one reaction, you should only produce one bullet. No need to have five bullets if I didn't have five highlights/reactions. 
3. If I have more than five highlights/reactions, then try to combine the highlights. 
4. Reactions should always be quoted verbatim. 
5. Drop the lower signal strength highlights to stick to the limit of five bullets.