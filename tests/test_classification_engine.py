from tools.finding_extractor import Finding
from core.classification_engine import classify_finding


def test_classifies_bola():
    finding = Finding(
        writeup_id="test-001",
        title="Example BOLA",
        vulnerabilities=["BOLA"],
    )

    result = classify_finding(finding)

    assert result.normalized_vulnerabilities == [
        "Broken Object Level Authorization"
    ]
    assert result.category.value == "API Security"
    assert result.owasp[0].value == "API1:2023"
    assert result.cwe[0].value == "CWE-639"
    assert result.cwe[0].status == "potential"


def test_normalizes_full_bola_name():
    finding = Finding(
        writeup_id="test-002",
        title="Example",
        vulnerabilities=[
            " broken object level authorization "
        ],
    )

    result = classify_finding(finding)

    assert result.normalized_vulnerabilities == [
        "Broken Object Level Authorization"
    ]


def test_classifies_idor_independently_from_bola():
    finding = Finding(
        writeup_id="test-003",
        title="Example IDOR",
        vulnerabilities=["IDOR"],
    )

    result = classify_finding(finding)

    assert result.normalized_vulnerabilities == [
        "Insecure Direct Object Reference"
    ]

    assert result.normalized_vulnerabilities != [
        "Broken Object Level Authorization"
    ]

    assert result.category.value == "Access Control"
    assert result.owasp[0].value == "A01:2025"

    assert result.cwe[0].value == "CWE-639"
    assert result.cwe[0].confidence == "medium"
    assert result.cwe[0].status == "potential"

def test_preserves_original_vulnerability_labels():
    finding = Finding(
        writeup_id="test-004",
        title="Example",
        vulnerabilities=["BOLA", "IDOR"],
    )

    result = classify_finding(finding)

    assert result.original_vulnerabilities == ["BOLA", "IDOR"]
    assert finding.vulnerabilities == ["BOLA", "IDOR"]


def test_unknown_vulnerability_is_not_classified():
    finding = Finding(
        writeup_id="test-005",
        title="Example",
        vulnerabilities=["Unknown Vulnerability"],
    )

    result = classify_finding(finding)

    assert result.normalized_vulnerabilities == []
    assert result.category is None
    assert result.owasp == []
    assert result.cwe == []

def test_preserves_source_report_classifications():
    finding = Finding(
        writeup_id="nextcloud-001",
        title="Nextcloud BOLA",
        vulnerabilities=["BOLA", "IDOR"],
    )

    source_classification = {
        "category": "api_security",
        "owasp": ["API1:2023"],
        "cwe": ["CWE-639", "CWE-862", "CWE-863"],
        "cve": [],
    }

    result = classify_finding(
        finding,
        source_classification,
    )

    assert result.source_report.category == "api_security"
    assert result.source_report.owasp == ["API1:2023"]
    assert result.source_report.cwe == [
        "CWE-639",
        "CWE-862",
        "CWE-863",
    ]


def test_separates_source_references_from_knowledge_base():
    finding = Finding(
        writeup_id="nextcloud-002",
        title="Nextcloud BOLA",
        vulnerabilities=["BOLA"],
    )

    source_classification = {
        "category": "api_security",
        "owasp": ["API1:2023"],
        "cwe": ["CWE-639", "CWE-862", "CWE-863"],
    }

    result = classify_finding(
        finding,
        source_classification,
    )

    assert result.source_report.cwe == [
        "CWE-639",
        "CWE-862",
        "CWE-863",
    ]

    assert [
        item.value for item in result.knowledge_base.cwe
    ] == ["CWE-639"]

    assert result.knowledge_base.cwe[0].status == "potential"


def test_source_classification_is_optional():
    finding = Finding(
        writeup_id="test-optional",
        title="Unknown vulnerability",
        vulnerabilities=["Unknown Vulnerability"],
    )

    result = classify_finding(finding)

    assert result.source_report.cwe == []
    assert result.source_report.owasp == []
    assert result.knowledge_base.category is None
