
from tools.writeup_parser import parse_writeup
from tools.finding_extractor import extract_finding


def test_extract_finding_from_writeup(tmp_path):
    content = """---
id: test-001
title: API BOLA
source:
  url: "https://example.com/report/1"
classification:
  vulnerability:
    - BOLA
    - IDOR
target:
  affected_endpoints:
    - method: GET
      path: /api/users/{userId}
severity:
  value: medium
verification:
  status: author_reported
  independently_reproduced: false
confidence: medium
---

# Executive Summary

BOLA vulnerability in the API.

# Technical Evidence

The server returns HTTP 200 when accessing another user's data.

# Impact Analysis

Unauthorized disclosure of personal information.

# Remediation

Implement object-level authorization.
"""

    file_path = tmp_path / "test-writeup.md"
    file_path.write_text(content, encoding="utf-8")

    document = parse_writeup(file_path)
    finding = extract_finding(document)

    assert finding.writeup_id == "test-001"
    assert finding.title == "API BOLA"
    assert finding.vulnerabilities == ["BOLA", "IDOR"]
    assert len(finding.endpoints) == 1
    assert finding.endpoints[0].method == "GET"
    assert finding.endpoints[0].path == "/api/users/{userId}"
    assert finding.severity == "medium"
    assert "Unauthorized disclosure" in finding.impact
    assert "HTTP 200" in finding.evidence
    assert finding.verification_status == "author_reported"
    assert finding.independently_reproduced is False
    assert finding.confidence == "medium"
    assert finding.source_url == "https://example.com/report/1"


def test_extract_finding_without_optional_sections(tmp_path):
    content = """---
id: test-002
title: Minimal finding
classification:
  vulnerability:
    - IDOR
target:
  affected_endpoints: []
severity:
  value: low
---

# Executive Summary

A minimal test finding.
"""

    file_path = tmp_path / "minimal-writeup.md"
    file_path.write_text(content, encoding="utf-8")

    document = parse_writeup(file_path)
    finding = extract_finding(document)

    assert finding.writeup_id == "test-002"
    assert finding.vulnerabilities == ["IDOR"]
    assert finding.endpoints == []
    assert finding.impact == ""
    assert finding.evidence == ""
    assert finding.source_url is None


def test_extract_sections_without_including_next_section(tmp_path):
    content = """---
id: test-003
title: Section boundary test
classification:
  vulnerability:
    - BOLA
target:
  affected_endpoints: []
---

# Technical Evidence

Evidence content.

# Impact Analysis

Impact content.

# Remediation

Remediation content.
"""

    file_path = tmp_path / "sections.md"
    file_path.write_text(content, encoding="utf-8")

    document = parse_writeup(file_path)
    finding = extract_finding(document)

    assert "Evidence content." in finding.evidence
    assert "Impact content." not in finding.evidence

    assert "Impact content." in finding.impact
    assert "Remediation content." not in finding.impact
