---
name: formlatex
description: Reflow overly long paragraph lines in .tex source files to a fixed column width, and/or convert leftover Markdown-style inline code spans (`text`) to italic LaTeX (\textit{text}), without changing any other content. Use when a LaTeX file has very long single-line paragraphs (e.g. one paragraph = one huge line) that make the source view hard to read or diff, and/or still contains Markdown backtick code spans left over from a Markdown source draft.
---

# formlatex

Two independent source-cleanup transformations for `.tex` files that were
drafted from Markdown or otherwise need reformatting, each safe to run
without changing the rendered output (beyond the intended formatting change
itself):

1. **Line wrapping** — reflows overly wide paragraph lines at word
   boundaries so the source is readable. LaTeX treats a single newline as
   whitespace, so rewrapping plain paragraph text is always safe as long as
   commands, comments, and blank lines are left untouched.
2. **Code-span conversion** — rewrites Markdown-style inline code spans
   left over from a Markdown draft (`` `FINISH_START` ``) into italic LaTeX
   (`\textit{FINISH\_START}`), since plain backticks aren't valid LaTeX
   markup and won't render as intended. No quote marks are added — italics
   alone already sets the span apart, and adding literal `"` quote marks on
   top is both redundant and unsafe in documents using babel's German
   shorthands (where `"` is an active character). Special characters inside
   the span (`_ # % & $ { } ~ ^ \`) are escaped automatically, since
   identifiers and paths often contain them (e.g. `_`) and a bare one
   outside math mode is a LaTeX error, not just a cosmetic issue — the
   original backticks hid this until conversion because backtick-delimited
   plain text still went through normal typesetting too, it just hadn't
   been noticed yet.

Run whichever transformation(s) the user asks for. If both are needed on
the same file, convert code spans first, then wrap — converting a span
changes the line's length and may push it past the wrap threshold.

## When to use

- A `.tex` file (or a selection within one) has paragraph lines that are
  hundreds or thousands of characters long on a single line, and the user
  wants the source view "formatted" / line-wrapped but explicitly does NOT
  want any wording, commands, or structure changed.
- A `.tex` file still has Markdown-style `` `code span` `` backtick markup
  (visible as literal backticks in the compiled PDF, or flagged by the user
  as "code highlighting from the Markdown template") and the user wants it
  turned into proper LaTeX italics.

## What NOT to touch

Never reflow (line wrapping):
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

Never convert (code spans):
- Comment lines — same reasoning as above.
- Fenced Markdown code blocks (` ```...``` `, e.g. a leftover directory-tree
  or code listing spanning multiple lines) — a single-backtick regex must
  not reach into multi-line fenced content; those blocks need converting to
  a proper `verbatim`/`lstlisting` environment by hand instead.
- Verbatim/listing environments — same reasoning as above.
- LaTeX's own backtick-quote idiom, `` `word' `` (opening backtick paired
  with a closing apostrophe, not another backtick) — the script's pattern
  requires a closing backtick, so this is never matched.

## How to do it

1. Identify the target file(s) and which transformation(s) are needed. If
   the user selected specific lines/a section, only process within that
   range.
2. Check for fenced code blocks and verbatim-like environments in the
   file; if present, confirm they'll be skipped correctly (both scripts
   already skip them automatically) or handle the file by hand instead.
3. Take a backup copy of the file so you can verify nothing unintended
   changed afterwards.
4. Run the bundled script(s) for the requested transformation(s). If doing
   both, convert code spans first, then wrap (see above for why):

   ```bash
   python "<skill_dir>/convert_codespans.py" "path/to/file.tex"
   python "<skill_dir>/wrap_tex.py" "path/to/file.tex" [width]
   ```

   Replace `<skill_dir>` with this skill's own directory (the folder
   containing this `SKILL.md`).

5. **Always verify the change matches intent** before considering the task
   done:
   - After wrapping only: compare the file before and after with
     whitespace collapsed to single spaces — they must be identical.
   - After code-span conversion (content intentionally changes, so a
     whitespace-collapsed diff won't be identical): spot-check that every
     remaining single-backtick pair outside fenced/verbatim regions was
     converted, and that fenced blocks/verbatim environments/comments were
     left untouched.

   Example whitespace-only check (for a wrap-only run):

   ```bash
   python -c "
import re
a = open('file.tex.bak', encoding='utf-8').read()
b = open('file.tex', encoding='utf-8').read()
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
print('IDENTICAL CONTENT' if norm(a) == norm(b) else 'DIFFERENT!')
"
   ```

   Delete the backup once verification passes.
6. Report what changed (new max line length for wrapping; number of code
   spans converted, for conversion) and confirm it was verified.
