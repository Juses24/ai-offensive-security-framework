
#!/usr/bin/env python3

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


FRONT_MATTER_PATTERN = re.compile(
    r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)",
    re.DOTALL,
)


class WriteupParseError(Exception):
    """Raised when a Markdown writeup cannot be parsed."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""

    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)

        mapping = {}

        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)

            if key in mapping:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"duplicate key: {key!r}",
                    key_node.start_mark,
                )

            mapping[key] = self.construct_object(
                value_node,
                deep=deep,
            )

        return mapping


@dataclass
class WriteupDocument:
    path: Path
    metadata: dict[str, Any]
    body: str


def parse_writeup(path: Path) -> WriteupDocument:
    """
    Parse a Markdown writeup into metadata and body.

    Extracts YAML Front Matter without validating
    the writeup schema.
    """

    if not path.is_file():
        raise WriteupParseError(f"File not found: {path}")

    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise WriteupParseError(
            f"Unable to read writeup: {exc}"
        ) from exc

    match = FRONT_MATTER_PATTERN.match(content)

    if not match:
        raise WriteupParseError("YAML Front Matter not found")

    try:
        metadata = yaml.load(
            match.group(1),
            Loader=UniqueKeyLoader,
        )
    except yaml.YAMLError as exc:
        raise WriteupParseError(
            f"Invalid YAML: {exc}"
        ) from exc

    if not isinstance(metadata, dict):
        raise WriteupParseError(
            "YAML Front Matter must contain a mapping"
        )

    body = content[match.end():].lstrip("\r\n")

    return WriteupDocument(
        path=path,
        metadata=metadata,
        body=body,
    )

