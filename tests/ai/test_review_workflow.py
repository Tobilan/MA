"""Regressionstests für Schema-Transformation und Review-Paket-Integrität."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


REPOSITORY = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY / "scripts" / "ai"))

from review_package import package_hash  # noqa: E402
from review_schema import (  # noqa: E402
    SchemaTransformationError,
    load_schema,
    to_claude_cli_schema,
)


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


class ReviewSchemaTests(unittest.TestCase):
    def test_canonical_schema_is_transformed_to_cli_subset(self) -> None:
        canonical = load_schema(REPOSITORY / "docs" / "ai" / "REVIEW_SCHEMA.json")
        transformed = to_claude_cli_schema(canonical)
        for node in walk(transformed):
            if isinstance(node, dict):
                self.assertNotIn("$ref", node)
                self.assertNotIn("$defs", node)
                self.assertNotIn("const", node)
                self.assertFalse(isinstance(node.get("type"), list))
        self.assertEqual(transformed["properties"]["schemaVersion"]["enum"], ["1.1"])
        finding = transformed["properties"]["findings"]["items"]
        self.assertEqual(
            finding["properties"]["lineStart"]["anyOf"],
            [{"type": "integer", "minimum": 1}, {"type": "null"}],
        )

    def test_unknown_keyword_on_type_array_is_rejected(self) -> None:
        schema = {"type": ["integer", "null"], "futureConstraint": 1}
        with self.assertRaises(SchemaTransformationError):
            to_claude_cli_schema(schema)

    def test_inapplicable_known_keyword_on_type_array_is_rejected(self) -> None:
        schema = {"type": ["integer", "null"], "pattern": "^[0-9]+$"}
        with self.assertRaises(SchemaTransformationError):
            to_claude_cli_schema(schema)

    def test_unknown_type_in_type_array_is_rejected_cleanly(self) -> None:
        schema = {"type": ["integer", "futureType"], "minimum": 1}
        with self.assertRaises(SchemaTransformationError):
            to_claude_cli_schema(schema)

    def test_applicable_constraint_is_preserved_only_where_semantic(self) -> None:
        schema = {"type": ["integer", "null"], "minimum": 1}
        self.assertEqual(
            to_claude_cli_schema(schema),
            {"anyOf": [{"type": "integer", "minimum": 1}, {"type": "null"}]},
        )


class ReviewPackageHashTests(unittest.TestCase):
    def test_prompt_and_schema_change_package_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary)
            files = {
                "changes.diff": "diff\n",
                "changed-files.json": "[]\n",
                "task.md": "Aufgabe\n",
                "review-config.json": "{}\n",
                "review-schema.json": "{}\n",
                "review-prompt.md": "Prompt A\n",
            }
            for name, content in files.items():
                (package / name).write_text(content, encoding="utf-8")
            (package / "metadata.json").write_text(
                json.dumps({"packageVersion": "1.2", "packageHash": "0" * 64}),
                encoding="utf-8",
            )
            initial = package_hash(package)
            (package / "review-prompt.md").write_text("Prompt B\n", encoding="utf-8")
            prompt_changed = package_hash(package)
            self.assertNotEqual(initial, prompt_changed)
            (package / "review-schema.json").write_text(
                '{"type":"object"}\n', encoding="utf-8"
            )
            self.assertNotEqual(prompt_changed, package_hash(package))


if __name__ == "__main__":
    unittest.main()
