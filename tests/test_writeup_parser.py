import pytest

from tools.writeup_parser import (
    WriteupParseError,
    parse_writeup,
)


def test_parse_valid_writeup(tmp_path):
    content = """---
id: test-001
title: Test Writeup
severity:
  value: high
tags:
  - api
  - bola
---

# Executive Summary

This is a test writeup.
"""

    file_path = tmp_path / "test-writeup.md"
    file_path.write_text(content, encoding="utf-8")

    document = parse_writeup(file_path)

    assert document.metadata["id"] == "test-001"
    assert document.metadata["title"] == "Test Writeup"
    assert document.metadata["severity"]["value"] == "high"
    assert document.metadata["tags"] == ["api", "bola"]
    assert "# Executive Summary" in document.body
    assert "This is a test writeup." in document.body


def test_parse_missing_front_matter(tmp_path):
    file_path = tmp_path / "invalid.md"
    file_path.write_text(
        "# Writeup without metadata",
        encoding="utf-8",
    )

    with pytest.raises(
        WriteupParseError,
        match="YAML Front Matter not found",
    ):
        parse_writeup(file_path)


def test_parse_invalid_yaml(tmp_path):
    content = """---
id: test-001
title: [invalid yaml
---
# Body
"""

    file_path = tmp_path / "invalid-yaml.md"
    file_path.write_text(content, encoding="utf-8")

    with pytest.raises(WriteupParseError, match="Invalid YAML"):
        parse_writeup(file_path)


def test_parse_non_mapping_front_matter(tmp_path):
    content = """---
- item1
- item2
---
# Body
"""

    file_path = tmp_path / "non-mapping.md"
    file_path.write_text(content, encoding="utf-8")

    with pytest.raises(
        WriteupParseError,
        match="must contain a mapping",
    ):
        parse_writeup(file_path)


def test_parse_missing_file(tmp_path):
    file_path = tmp_path / "does-not-exist.md"

    with pytest.raises(WriteupParseError, match="File not found"):
        parse_writeup(file_path)

def test_parse_duplicate_yaml_keys(tmp_path):
    content = """---
id: test-001
title: Original Title
title: Overwritten Title
---
# Body
"""

    file_path = tmp_path / "duplicate-keys.md"
    file_path.write_text(content, encoding="utf-8")

    with pytest.raises(
        WriteupParseError,
        match="Invalid YAML",
    ):
        parse_writeup(file_path)


def test_parse_invalid_utf8(tmp_path):
    file_path = tmp_path / "invalid-encoding.md"
    file_path.write_bytes(b"---\nid: test-001\n---\n\xff")

    with pytest.raises(
        WriteupParseError,
        match="Unable to read",
    ):
        parse_writeup(file_path)
