
from pathlib import Path

from tools.writeup_validator import validate_writeup


VALID_WRITEUP = """\
---
schema_version: "1.0"
id: "test-writeup-001"
title: "Test Writeup"

source:
  platform: "hackerone"
  url: "https://example.com/report"

target:
  name: "Example"
  affected_versions: []
  affected_endpoints: []

classification:
  category: "api_security"
  vulnerability: []
  owasp: []
  cwe: []
  cve: []

severity:
  value: "medium"

verification:
  status: "author_reported"
  independently_reproduced: false

confidence: "medium"

intelligence:
  attack_surface: []
  techniques: []
  detection_patterns: []
  related_vulnerabilities: []
  potential_chains: []

research:
  status: "analyzed"
  created_at: "2026-11-11"
  updated_at: "2026-11-11"
---
# Test Writeup
"""


def test_valid_writeup(tmp_path: Path):
    file_path = tmp_path / "valid.md"
    file_path.write_text(VALID_WRITEUP, encoding="utf-8")

    assert validate_writeup(file_path) == []


def test_missing_fields_and_empty_id(tmp_path: Path):
    file_path = tmp_path / "invalid.md"
    file_path.write_text(
        '---\nschema_version: "1.0"\nid: ""\ntitle: "Invalid"\n---\n',
        encoding="utf-8",
    )

    errors = validate_writeup(file_path)

    assert "Missing required field: source" in errors
    assert "Field 'id' cannot be empty" in errors


def test_missing_front_matter(tmp_path: Path):
    file_path = tmp_path / "no_front_matter.md"
    file_path.write_text("# No YAML here\n", encoding="utf-8")

    errors = validate_writeup(file_path)

    assert "YAML Front Matter not found" in errors


def test_invalid_http_endpoint(tmp_path: Path):
    invalid_writeup = VALID_WRITEUP.replace(
        "affected_endpoints: []",
        'affected_endpoints:\n'
        '  - method: "INVALID"\n'
        '    path: "users"'
    )

    file_path = tmp_path / "invalid_endpoint.md"
    file_path.write_text(invalid_writeup, encoding="utf-8")

    errors = validate_writeup(file_path)

    assert "Invalid HTTP method at endpoint index 0" in errors
    assert "Invalid endpoint path at index 0" in errors

def test_invalid_severity(tmp_path: Path):
    invalid_writeup = VALID_WRITEUP.replace(
        'value: "medium"',
        'value: "extreme"'
    )

    file_path = tmp_path / "invalid_severity.md"
    file_path.write_text(invalid_writeup, encoding="utf-8")

    errors = validate_writeup(file_path)

    assert "Invalid severity value: extreme" in errors


def test_invalid_verification_status(tmp_path: Path):
    invalid_writeup = VALID_WRITEUP.replace(
        'status: "author_reported"',
        'status: "unverified"'
    )

    file_path = tmp_path / "invalid_verification.md"
    file_path.write_text(invalid_writeup, encoding="utf-8")

    errors = validate_writeup(file_path)

    assert "Invalid verification status: unverified" in errors


def test_inconsistent_analyzed_verification(tmp_path: Path):
    invalid_writeup = VALID_WRITEUP.replace(
        "independently_reproduced: false",
        "independently_reproduced: true"
    )

    file_path = tmp_path / "inconsistent_analyzed.md"
    file_path.write_text(invalid_writeup, encoding="utf-8")

    errors = validate_writeup(file_path)

    assert any(
        "cannot have independently_reproduced=True" in error
        for error in errors
    )


def test_independent_reproduction_requires_true(tmp_path: Path):
    invalid_writeup = VALID_WRITEUP.replace(
        'status: "author_reported"',
        'status: "independently_reproduced"'
    )

    file_path = tmp_path / "inconsistent_reproduction.md"
    file_path.write_text(invalid_writeup, encoding="utf-8")

    errors = validate_writeup(file_path)

    assert any(
        "'independently_reproduced' requires" in error
        for error in errors
    )
