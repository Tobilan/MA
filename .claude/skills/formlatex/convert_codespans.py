"""Converts Markdown-style inline code spans in a .tex file to italic LaTeX.

Usage: python convert_codespans.py <path-to-tex-file>

Leftover Markdown formatting such as `FINISH_START` (backtick-delimited,
single-line code spans) is rewritten as \\textit{FINISH\\_START}. No quote
marks are added - \\textit already sets the span apart from surrounding
text, so wrapping it in quotes on top is redundant (and was previously a
source of bugs: literal `"` quote marks are unsafe in documents using
babel's German shorthands, see git history).

Code spans commonly contain identifiers, paths or filenames with characters
that are special to LaTeX (most often `_`, as in FINISH_START) - unlike
inside the original backticks, those characters are typeset as normal text
once wrapped in \\textit{...}, so they are escaped to keep the result
compiling (a bare `_` outside math mode is a LaTeX error, not just a
rendering quirk).

Left untouched:
- Comment lines (start with %, ignoring leading whitespace).
- Fenced code blocks (```...``` / ```lang ... ```), since a single-backtick
  regex must not reach into multi-line fenced content.
- verbatim/lstlisting/minted environments, for the same reason.
- LaTeX's own backtick-quote usage (`` `word' ``, opening backtick + closing
  apostrophe) is never matched, since the pattern requires a closing
  backtick, not an apostrophe.
"""

import re
import sys

CODESPAN_RE = re.compile(r"`([^`\n]+)`")
FENCE_RE = re.compile(r"^\s*```")
ENV_BEGIN_RE = re.compile(r"\\begin\{(verbatim|lstlisting|minted\*?)\}")
ENV_END_RE = re.compile(r"\\end\{(verbatim|lstlisting|minted\*?)\}")

# Order matters: backslash must be escaped first, or the backslashes
# introduced by later replacements would themselves get re-escaped.
LATEX_SPECIAL_CHARS = [
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
    ("$", r"\$"),
    ("#", r"\#"),
    ("_", r"\_"),
    ("{", r"\{"),
    ("}", r"\}"),
    ("~", r"\textasciitilde{}"),
    ("^", r"\textasciicircum{}"),
]


def escape_latex(text: str) -> str:
    for char, escaped in LATEX_SPECIAL_CHARS:
        text = text.replace(char, escaped)
    return text


def convert_line(line: str) -> str:
    return CODESPAN_RE.sub(lambda m: r"\textit{" + escape_latex(m.group(1)) + "}", line)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python convert_codespans.py <path-to-tex-file>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    out_lines = []
    in_fence = False
    in_env = False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue
        if ENV_BEGIN_RE.search(line):
            in_env = True
            out_lines.append(line)
            continue
        if ENV_END_RE.search(line):
            in_env = False
            out_lines.append(line)
            continue
        if in_env or line.lstrip().startswith("%"):
            out_lines.append(line)
            continue
        out_lines.append(convert_line(line))

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.writelines(out_lines)


if __name__ == "__main__":
    main()
