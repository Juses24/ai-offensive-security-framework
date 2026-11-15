from core.pipeline import process_writeup


def create_test_writeup(tmp_path):
    content = """---
schema_version: "1.0"
id: "pipeline-test-001"
title: "Example BOLA Finding"

source:
  platform: "hackerone"

target:
  affected_endpoints:
    - method: "GET"
      path: "/api/users/{id}"

classification:
  category: "api_security"
  vulnerability:
    - "BOLA"
    - "IDOR"
  owasp:
    - "API1:2023"
  cwe:
    - "CWE-639"
    - "CWE-862"
    - "CWE-863"

severity:
  value: "medium"

verification:
  status: "author_reported"
  independently_reproduced: false

confidence: "medium"
---

# Impact Analysis

Unauthorized access to another user's information.

# Technical Evidence

A modified object identifier returns another user's data.
"""

    path = tmp_path / "test-writeup.md"
    path.write_text(content, encoding="utf-8")

    return path


def test_pipeline_processes_writeup(tmp_path):
    path = create_test_writeup(tmp_path)

    result = process_writeup(path)

    assert result.finding.writeup_id == "pipeline-test-001"
    assert result.finding.vulnerabilities == ["BOLA", "IDOR"]

    assert result.classification.normalized_vulnerabilities == [
        "Broken Object Level Authorization"
    ]


def test_pipeline_preserves_source_classifications(tmp_path):
    path = create_test_writeup(tmp_path)

    result = process_writeup(path)

    assert result.classification.source_report.category == "api_security"

    assert result.classification.source_report.owasp == [
        "API1:2023"
    ]

    assert result.classification.source_report.cwe == [
        "CWE-639",
        "CWE-862",
        "CWE-863",
    ]


def test_pipeline_preserves_verification_status(tmp_path):
    path = create_test_writeup(tmp_path)

    result = process_writeup(path)

    assert result.finding.verification_status == "author_reported"
    assert result.finding.independently_reproduced is False

    assert result.classification.knowledge_base.cwe[0].status == "potential"
