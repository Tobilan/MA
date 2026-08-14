---
name: formlatex
description: Reflow overly long paragraph lines in .tex source files to a fixed column width, without changing any content. Use when a LaTeX file has very long single-line paragraphs (e.g. one paragraph = one huge line) that make the source view hard to read or diff, and the user wants the lines wrapped/formatted while the rendered document and text stay exactly the same.
---

# formlatex

Wraps overly wide paragraph lines in `.tex` files at word boundaries so the
source is readable, without altering any content. LaTeX treats a single
newline as whitespace, so rewrapping plain paragraph text is always safe as
long as commands, comments, and blank lines are left untouched.

## When to use

- A `.tex` file (or a selection within one) has paragraph lines that are
  hundreds or thousands of characters long on a single line.
- The user wants the source view "formatted" / line-wrapped but explicitly
  does NOT want any wording, commands, or structure changed.

## What NOT to touch

Never reflow:
- Comment lines (start with `%`, possibly after leading whitespace) —
  wrapping these without re-adding `%` on every continuation line would
  turn text into live LaTeX code.
- Command / structural lines such as `\section{...}`, `\subsection{...}`,
  `\label{...}`, `\setcounter{...}`, etc. — leave them on one line even if
  long.
- Blank lines (they separate paragraphs — must be preserved exactly).
- Verbatim/listing environments (`verbatim`, `lstlisting`, `minted`, ...) —
  never touch content inside these; whitespace is significant there.

Only plain prose paragraph lines above a length threshold (default 200
characters) are candidates for reflow.

## How to do it

1. Identify the target file(s). If the user selected specific lines/a
   section, only reflow within that range.
2. Check for verbatim-like environments in the file; if present, exclude
   those ranges from processing (or handle the file by hand instead of
   using the bundled script).
3. Run the bundled script, which wraps only long, non-comment lines at
   word boundaries (default width 100 columns, no hyphenation, no word
   splitting):

   ```bash
   python "<skill_dir>/wrap_tex.py" "path/to/file.tex" [width]
   ```

   Replace `<skill_dir>` with this skill's own directory (the folder
   containing this `SKILL.md`).

4. **Always verify no content changed** before considering the task done:
   compare the file before and after with whitespace collapsed to single
   spaces — they must be identical. Example check:

   ```bash
   python -c "
import re
a = open('file.tex.bak', encoding='utf-8').read()
b = open('file.tex', encoding='utf-8').read()
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
print('IDENTICAL CONTENT' if norm(a) == norm(b) else 'DIFFERENT!')
"
   ```

   Take a backup copy before running the script so this comparison is
   possible, and delete the backup once the check passes.
5. Report the new max line length and confirm content was verified
   unchanged.
