#!/usr/bin/env python3
"""
Validate whether a file looks like usable draw.io XML.

Usage:
    python3 validate_drawio_xml.py path/to/file.drawio
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


VALID_ROOTS = {"mxfile", "mxGraphModel"}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 validate_drawio_xml.py <drawio-file>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"[ERROR] File not found: {path}", file=sys.stderr)
        return 1

    try:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
    except ET.ParseError as exc:
        print(f"[ERROR] XML parse failed: {exc}", file=sys.stderr)
        return 1

    if root.tag not in VALID_ROOTS:
        print(
            f"[ERROR] Unexpected root tag '{root.tag}'. Expected one of: {', '.join(sorted(VALID_ROOTS))}",
            file=sys.stderr,
        )
        return 1

    if root.tag == "mxfile":
        diagram = root.find("diagram")
        if diagram is None:
            print("[ERROR] mxfile is missing a <diagram> child.", file=sys.stderr)
            return 1
        model = diagram.find("mxGraphModel")
        if model is None:
            print("[ERROR] <diagram> is missing <mxGraphModel>.", file=sys.stderr)
            return 1
        root_node = model.find("root")
    else:
        root_node = root.find("root")

    if root_node is None:
        print("[ERROR] Missing <root> element in mxGraphModel.", file=sys.stderr)
        return 1

    ids = {cell.attrib.get("id") for cell in root_node.findall("mxCell")}
    if "0" not in ids or "1" not in ids:
        print("[ERROR] Expected base mxCell ids '0' and '1' were not found.", file=sys.stderr)
        return 1

    print(f"[OK] {path} looks like valid draw.io XML with root <{root.tag}>.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

