#!/usr/bin/env python3

import argparse
from pathlib import Path

from core.pipeline import process_writeup


def format_value(value):
    """Format classification mappings and ordinary values."""
    return getattr(value, "value", value)


def format_list(values):
    """Format a list of classification values."""
    return ", ".join(str(format_value(value)) for value in values) or "None"


def display_result(result):
    finding = result.finding
    classification = result.classification

    print("\n========== AI-OSF ==========")
    print("Writeup processed successfully.")

    print("\n[Finding]")
    print(f"ID: {finding.writeup_id}")
    print(f"Title: {finding.title}")
    print(f"Vulnerabilities: {format_list(finding.vulnerabilities)}")
    print(f"Severity: {finding.severity}")
    print(f"Verification: {finding.verification_status}")
    print(
        f"Independently reproduced: "
        f"{finding.independently_reproduced}"
    )

    print("\n[Source Report]")
    source = classification.source_report
    print(f"Category: {source.category}")
    print(f"OWASP: {format_list(source.owasp)}")
    print(f"CWE: {format_list(source.cwe)}")

    print("\n[AI-OSF Knowledge Base]")
    knowledge = classification.knowledge_base
    print(f"Normalized vulnerabilities: "
          f"{format_list(classification.normalized_vulnerabilities)}")
    print(f"Category: {format_value(knowledge.category)}")
    print(f"OWASP: {format_list(knowledge.owasp)}")
    print(f"CWE: {format_list(knowledge.cwe)}")

    print("\n[Related Concepts]")
    print(format_list(classification.related_concepts))

    print("\n============================")


def main():
    parser = argparse.ArgumentParser(
        prog="ai-osf",
        description="AI Offensive Security Framework CLI",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    process_parser = subparsers.add_parser(
        "process",
        help="Process a security writeup",
    )

    process_parser.add_argument(
        "writeup",
        type=Path,
        help="Path to the Markdown writeup",
    )

    args = parser.parse_args()

    if args.command == "process":
        try:
            result = process_writeup(args.writeup)
            display_result(result)
            return 0

        except Exception as error:
            print(f"[ERROR] {error}")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
