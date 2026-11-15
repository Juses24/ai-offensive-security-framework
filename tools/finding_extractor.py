
#!/usr/bin/env python3

import re
from dataclasses import dataclass, field
from typing import Any

from tools.writeup_parser import WriteupDocument


@dataclass
class Endpoint:
    method: str
    path: str


@dataclass
class Finding:
    writeup_id: str
    title: str
    vulnerabilities: list[str] = field(default_factory=list)
    endpoints: list[Endpoint] = field(default_factory=list)
    severity: str = "unknown"
    impact: str = ""
    evidence: str = ""
    verification_status: str = "unknown"
    independently_reproduced: bool = False
    confidence: str = "unknown"
    source_url: str | None = None


def extract_section(body: str, heading: str) -> str:
    """
    Extract a Markdown section by heading.

    Stops at the next heading of the same or higher level.
    """

    pattern = re.compile(
        rf"^#{{1,6}}\s+{re.escape(heading)}\s*$"
        rf"(.*?)(?=^#{{1,6}}\s+|\Z)",
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )

    match = pattern.search(body)

    if not match:
        return ""

    return match.group(1).strip()


def extract_finding(document: WriteupDocument) -> Finding:
    """
    Extract structured vulnerability information
    from a parsed writeup.
    """

    metadata: dict[str, Any] = document.metadata

    classification = metadata.get("classification") or {}
    target = metadata.get("target") or {}
    severity = metadata.get("severity") or {}
    verification = metadata.get("verification") or {}
    source = metadata.get("source") or {}

    vulnerabilities = classification.get("vulnerability") or []

    if isinstance(vulnerabilities, str):
        vulnerabilities = [vulnerabilities]

    endpoints = []

    for item in target.get("affected_endpoints") or []:
        if not isinstance(item, dict):
            continue

        endpoints.append(
            Endpoint(
                method=str(item.get("method", "")).upper(),
                path=str(item.get("path", "")),
            )
        )

    independently_reproduced = verification.get(
        "independently_reproduced",
        False,
    )

    if not isinstance(independently_reproduced, bool):
        independently_reproduced = False

    return Finding(
        writeup_id=str(metadata.get("id", "")),
        title=str(metadata.get("title", "")),
        vulnerabilities=list(vulnerabilities),
        endpoints=endpoints,
        severity=str(severity.get("value", "unknown")),
        impact=extract_section(document.body, "Impact Analysis"),
        evidence=extract_section(document.body, "Technical Evidence"),
        verification_status=str(
            verification.get("status", "unknown")
        ),
        independently_reproduced=independently_reproduced,
        confidence=str(metadata.get("confidence", "unknown")),
        source_url=source.get("url"),
    )
