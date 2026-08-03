#!/usr/bin/env python3
"""Berechnet stabile Integritätskennungen für Review-Pakete."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


CORE_FILES = (
    "changes.diff",
    "changed-files.json",
    "task.md",
    "review-config.json",
    "review-schema.json",
    "review-prompt.md",
    "external-evidence.json",
)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def package_hash(package: Path) -> str:
    """Hasht Review-Eingaben und Metadaten ohne das zirkuläre packageHash-Feld."""

    digest = hashlib.sha256()
    names = [name for name in CORE_FILES if (package / name).is_file()]
    names.extend(sorted(path.name for path in package.glob("claim-inventory.*") if path.is_file()))
    metadata_path = package / "metadata.json"
    if not metadata_path.is_file():
        raise ValueError("metadata.json fehlt im Review-Paket.")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict):
        raise ValueError("metadata.json muss ein JSON-Objekt sein.")
    metadata = dict(metadata)
    metadata.pop("packageHash", None)
    metadata_bytes = json.dumps(
        metadata, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    entries = [("metadata.json", metadata_bytes)]
    entries.extend((name, (package / name).read_bytes()) for name in sorted(set(names)))
    for name, payload in entries:
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()
