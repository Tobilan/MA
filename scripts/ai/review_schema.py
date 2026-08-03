#!/usr/bin/env python3
"""Erzeugt aus dem kanonischen Review-Schema ein Claude-CLI-kompatibles Schema."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


ANNOTATION_KEYS = {"$schema", "$id", "title", "description", "examples", "default"}
SUPPORTED_KEYS = {
    "type",
    "properties",
    "required",
    "additionalProperties",
    "items",
    "enum",
    "anyOf",
    "allOf",
    "oneOf",
    "pattern",
    "minLength",
    "maxLength",
    "minimum",
    "maximum",
    "minItems",
    "maxItems",
    "uniqueItems",
}
TYPE_SPECIFIC_KEYS = {
    "null": {"enum"},
    "string": {"pattern", "minLength", "maxLength", "enum"},
    "integer": {"minimum", "maximum", "enum"},
    "number": {"minimum", "maximum", "enum"},
    "array": {"items", "minItems", "maxItems", "uniqueItems"},
    "object": {"properties", "required", "additionalProperties"},
    "boolean": {"enum"},
}


class SchemaTransformationError(ValueError):
    """Das kanonische Schema kann nicht verlustarm transformiert werden."""


def load_schema(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SchemaTransformationError(f"Schema kann nicht gelesen werden: {exc}") from exc
    if not isinstance(value, dict):
        raise SchemaTransformationError("Das kanonische Schema muss ein JSON-Objekt sein.")
    return value


def _resolve_pointer(root: dict[str, Any], reference: str) -> Any:
    if not reference.startswith("#/"):
        raise SchemaTransformationError(
            f"Nur lokale JSON-Pointer werden unterstützt, erhalten: {reference}"
        )
    current: Any = root
    for token in reference[2:].split("/"):
        key = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or key not in current:
            raise SchemaTransformationError(f"Schema-Referenz kann nicht aufgelöst werden: {reference}")
        current = current[key]
    return current


def _transform(
    node: Any,
    root: dict[str, Any],
    reference_stack: tuple[str, ...] = (),
) -> Any:
    if isinstance(node, list):
        return [_transform(item, root, reference_stack) for item in node]
    if not isinstance(node, dict):
        return copy.deepcopy(node)

    if "$ref" in node:
        reference = node["$ref"]
        if not isinstance(reference, str):
            raise SchemaTransformationError("$ref muss eine Zeichenkette sein.")
        if reference in reference_stack:
            raise SchemaTransformationError(f"Zyklische Schema-Referenz: {reference}")
        resolved = copy.deepcopy(_resolve_pointer(root, reference))
        siblings = {key: value for key, value in node.items() if key != "$ref"}
        if siblings:
            if not isinstance(resolved, dict):
                raise SchemaTransformationError("$ref mit Nachbareigenschaften verweist nicht auf ein Objekt.")
            resolved.update(siblings)
        return _transform(resolved, root, (*reference_stack, reference))

    working = {key: value for key, value in node.items() if key not in ANNOTATION_KEYS}
    working.pop("$defs", None)
    if "const" in working:
        if "enum" in working:
            raise SchemaTransformationError("Ein Schemaelement enthält gleichzeitig const und enum.")
        working["enum"] = [working.pop("const")]

    declared_type = working.get("type")
    if isinstance(declared_type, list):
        if not declared_type or not all(isinstance(item, str) for item in declared_type):
            raise SchemaTransformationError("Mehrfachtypen müssen nicht leere String-Arrays sein.")
        for item_type in declared_type:
            if item_type not in TYPE_SPECIFIC_KEYS:
                raise SchemaTransformationError(f"Nicht unterstützter JSON-Typ: {item_type}")
        siblings = {key: value for key, value in working.items() if key != "type"}
        combinators = {"allOf", "anyOf", "oneOf"}
        for key in siblings:
            if key not in SUPPORTED_KEYS:
                raise SchemaTransformationError(
                    f"Nicht unterstütztes kanonisches Schema-Schlüsselwort: {key}"
                )
            if key not in combinators and not any(
                key in TYPE_SPECIFIC_KEYS[item_type] for item_type in declared_type
            ):
                raise SchemaTransformationError(
                    f"Schema-Schlüsselwort {key} ist auf keinen Typ in {declared_type} anwendbar."
                )
        variants: list[dict[str, Any]] = []
        for item_type in declared_type:
            permitted = TYPE_SPECIFIC_KEYS[item_type]
            variant = {"type": item_type}
            for key, value in siblings.items():
                if key in permitted or key in combinators:
                    variant[key] = _transform(value, root, reference_stack)
            variants.append(variant)
        return {"anyOf": variants}

    result: dict[str, Any] = {}
    for key, value in working.items():
        if key not in SUPPORTED_KEYS:
            raise SchemaTransformationError(
                f"Nicht unterstütztes kanonisches Schema-Schlüsselwort: {key}"
            )
        if key == "properties":
            if not isinstance(value, dict):
                raise SchemaTransformationError("properties muss ein Objekt sein.")
            result[key] = {
                name: _transform(property_schema, root, reference_stack)
                for name, property_schema in value.items()
            }
        else:
            result[key] = _transform(value, root, reference_stack)
    return result


def to_claude_cli_schema(canonical_schema: dict[str, Any]) -> dict[str, Any]:
    """Transformiert die verwendete Draft-2020-12-Teilmenge ohne Fallback."""

    transformed = _transform(canonical_schema, canonical_schema)
    if not isinstance(transformed, dict):
        raise SchemaTransformationError("Das transformierte Schema ist kein JSON-Objekt.")
    assert_cli_compatible(transformed)
    return transformed


def assert_cli_compatible(node: Any, location: str = "Wurzel") -> None:
    if isinstance(node, list):
        for index, item in enumerate(node):
            assert_cli_compatible(item, f"{location}[{index}]")
        return
    if not isinstance(node, dict):
        return
    for key, value in node.items():
        if key.startswith("$") or key == "const":
            raise SchemaTransformationError(f"{location}: CLI-inkompatibles Schlüsselwort {key}.")
        if key == "type" and isinstance(value, list):
            raise SchemaTransformationError(f"{location}.type: Typ-Arrays sind nicht CLI-kompatibel.")
        assert_cli_compatible(value, f"{location}.{key}")


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def schema_hash(value: Any) -> str:
    return hashlib.sha256(compact_json(value).encode("utf-8")).hexdigest()
