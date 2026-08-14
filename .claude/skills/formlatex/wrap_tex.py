"""Reflows overly long paragraph lines in a .tex file to a fixed column width.

Usage: python wrap_tex.py <path-to-tex-file> [width]

Only lines longer than 200 characters that are not comment lines
(do not start with %, ignoring leading whitespace) are reflowed.
Everything else (commands, labels, comments, blank lines, already-short
lines) is left byte-for-byte unchanged. Words are never split and no
hyphens are inserted, so the reflow only changes where line breaks fall
- never the actual text content.
"""

import sys
import textwrap

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python wrap_tex.py <path-to-tex-file> [width]", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    threshold = 200

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    out_lines = []
    for line in lines:
        stripped = line.rstrip("\n")
        if len(stripped) > threshold and not stripped.lstrip().startswith("%"):
            wrapped = textwrap.wrap(
                stripped,
                width=width,
                break_long_words=False,
                break_on_hyphens=False,
            )
            out_lines.extend(w + "\n" for w in wrapped)
        else:
            out_lines.append(line)

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.writelines(out_lines)

if __name__ == "__main__":
    main()
