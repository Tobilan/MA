#!/usr/bin/env bash
# Converts all .mmd files in meermaid/ to .pdf files in ../pics/
#
# PDFs are rendered directly by mermaid-cli's headless Chromium backend
# rather than routed through Inkscape (as a plain .svg + \includesvg would
# be). Inkscape's SVG text/tspan importer drops inter-word spacing and
# glyphs (e.g. arrows) that mermaid positions via per-word <tspan> offsets,
# since it re-flows the text with substituted fonts instead of honoring the
# original positions. Chromium prints the diagram exactly as rendered in a
# browser, so spacing, fonts and special characters stay correct.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PICS_DIR="$SCRIPT_DIR/../pics"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$PICS_DIR"

for mmd_file in "$SCRIPT_DIR"/*.mmd; do
    [ -e "$mmd_file" ] || continue
    name="$(basename "${mmd_file%.mmd}")"
    tmp_file="$TMP_DIR/$name.mmd"

    # Strip optional ```mermaid / ``` code-fence lines before conversion
    sed -e '1{/^```mermaid$/d}' -e '${/^```$/d}' "$mmd_file" > "$tmp_file"

    echo "Converting $name.mmd -> pics/$name.pdf"
    npx -y @mermaid-js/mermaid-cli -i "$tmp_file" -o "$PICS_DIR/$name.pdf" -c "$SCRIPT_DIR/mermaid-config.json" --pdfFit
done

echo "Done."
