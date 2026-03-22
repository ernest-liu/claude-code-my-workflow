---
name: de-ai
description: "Remove AI-sounding patterns from academic writing. Makes minimal changes to sound like a thoughtful human expert while preserving structure, content, and citations. Use when user says \"de-AI\", \"sounds too AI\", \"make it sound human\", \"polish prose\", or wants to clean up AI-generated text."
argument-hint: "[file.tex or file.md, or paste text directly]"
allowed-tools: ["Read", "Edit", "Write", "Glob", "Grep"]
---

# De-AI: Remove AI Writing Patterns

Make minimal changes to academic text so it reads as written by a thoughtful human expert. Preserve structure, content, and meaning — only fix the most obvious AI patterns.

## Context: $ARGUMENTS

## Step 1: Identify the Input

- If $ARGUMENTS is a file path: read the file
- If $ARGUMENTS is pasted text: work with it directly
- If a .tex file: preserve all LaTeX commands, environments, and formatting
- If a .md file: preserve all markdown formatting

## Step 2: Apply the De-AI Rewrite

Rewrite the text following these rules precisely:

### Sentence rhythm
- Vary sentence length where it feels unnatural — mix short punchy sentences with longer ones
- Do NOT force variation where the original already reads well

### Hedging and qualification
- PRESERVE all hedging language that reflects genuine epistemic uncertainty (e.g., "may", "suggests", "it is possible that")
- Do NOT flatten careful qualifications — these are features of good academic writing, not AI artifacts

### Register
- Maintain a formal academic register throughout
- No colloquialisms or informality

### AI phrase replacement
Replace these generic "AI-ish" phrases with direct academic language:

| AI Pattern | Replace With |
|---|---|
| "it is important to note" | (delete, or state the point directly) |
| "in conclusion" | (use a substantive transition) |
| "delve into" | "examine", "analyze", "study" |
| "it is worth mentioning" | (delete, just mention it) |
| "plays a crucial role" | (be specific about the role) |
| "a wide range of" | (be specific, or just "various") |
| "in the realm of" | "in" |
| "it should be noted that" | (delete, just state it) |
| "this is particularly relevant" | (delete, or explain why) |
| "a comprehensive analysis" | (just describe what the analysis does) |
| "leverage" (as verb) | "use", "exploit", "take advantage of" |
| "robust" (when vague) | (be specific about what makes it robust) |
| "shed light on" | "clarify", "reveal", "explain" |
| "pave the way for" | "enable", "make possible" |
| "the landscape of" | (delete) |
| "a nuanced understanding" | (describe the understanding) |
| "in this context" | (delete if context is already clear) |

### List structures
- Break up overly parallel list structures only where they read as conspicuously mechanical
- Not all lists are AI artifacts — preserve lists that serve the argument

### Specificity
- Add concrete examples, numbers, or named references only where it fits naturally
- Do NOT fabricate — if you don't know the specific detail, leave the general statement

### Content integrity
- PRESERVE all technical content, claims, and citations exactly
- Do NOT alter facts, results, or attributions
- Do NOT add filler or pad length
- Do NOT change notation conventions

## Step 3: Output

- If the input was a file: edit the file in place with the changes
- If the input was pasted text: return only the rewritten text, no commentary
- For files, show a brief summary of what was changed (e.g., "12 AI phrases replaced, 3 sentences restructured")

## Key Rules

- **Minimal changes** — this is editing, not rewriting. If a sentence reads fine, leave it alone.
- **Preserve the author's voice** — don't impose a new style, just remove the AI veneer
- **When in doubt, don't change it** — a false positive (changing good prose) is worse than a false negative (missing an AI pattern)
- **No commentary in output** — return only the rewritten text (for pasted input) or edit silently (for files)
