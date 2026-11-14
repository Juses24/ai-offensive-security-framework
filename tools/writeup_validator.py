
#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path

import yaml


REQUIRED_FIELDS = {
    "schema_version": str,
    "id": str,
    "title": str,
    "source": dict,
    "target": dict,
    "classification": dict,
    "severity": dict,
    "verification": dict,
    "confidence": str,
    "intelligence": dict,
    "research": dict,
}

NESTED_FIELDS = {
    "source": {
        "platform": str,
        "url": str,
    },
    "target": {
        "name": str,
        "affected_versions": list,
        "affected_endpoints": list,
    },
    "classification": {
        "category": str,
        "vulnerability": list,
        "owasp": list,
        "cwe": list,
        "cve": list,
    },
    "severity": {
        "value": str,
    },
    "verification": {
        "status": str,
        "independently_reproduced": bool,
    },
    "intelligence": {
        "attack_surface": list,
        "techniques": list,
        "detection_patterns": list,
        "related_vulnerabilities": list,
        "potential_chains": list,
    },
    "research": {
        "status": str,
        "created_at": str,
        "updated_at": str,
    },
}



def validate_writeup(path: Path) -> list[str]:
    errors = []

    # 1. Verify that the file exists
    if not path.is_file():
        return [f"File not found: {path}"]

    # 2. Read Markdown content
    content = path.read_text(encoding="utf-8")

    # 3. Extract YAML Front Matter
    match = re.match(
        r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)",
        content,
        re.DOTALL,
    )

    if not match:
        return ["YAML Front Matter not found"]

    # 4. Parse YAML
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return [f"Invalid YAML: {exc}"]

    if not isinstance(metadata, dict):
        return ["YAML Front Matter must contain a mapping"]

    # 5. Validate HTTP endpoints
    target = metadata.get("target")

    if isinstance(target, dict):
        endpoints = target.get("affected_endpoints")

        if isinstance(endpoints, list):
            allowed_methods = {
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
                "OPTIONS",
                "HEAD",
            }

            for index, endpoint in enumerate(endpoints):
                if not isinstance(endpoint, dict):
                    errors.append(
                        f"Invalid endpoint at index {index}: expected mapping"
                    )
                    continue

                method = endpoint.get("method")
                endpoint_path = endpoint.get("path")

                if (
                    not isinstance(method, str)
                    or method.upper() not in allowed_methods
                ):
                    errors.append(
                        f"Invalid HTTP method at endpoint index {index}"
                    )

                if (
                    not isinstance(endpoint_path, str)
                    or not endpoint_path.startswith("/")
                ):
                    errors.append(
                        f"Invalid endpoint path at index {index}"
                    )

    # 6. Validate required top-level fields
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in metadata:
            errors.append(f"Missing required field: {field}")

        elif not isinstance(metadata[field], expected_type):
            errors.append(
                f"Invalid type for '{field}': "
                f"expected {expected_type.__name__}"
            )

    # Validate non-empty ID
    writeup_id = metadata.get("id")

    if isinstance(writeup_id, str) and not writeup_id.strip():
        errors.append("Field 'id' cannot be empty")

    # 7. Validate nested fields
    for section, fields in NESTED_FIELDS.items():
        section_data = metadata.get(section)

        if not isinstance(section_data, dict):
            continue

        for field, expected_type in fields.items():
            if field not in section_data:
                errors.append(f"Missing field: {section}.{field}")

            elif not isinstance(section_data[field], expected_type):
                errors.append(
                    f"Invalid type for '{section}.{field}': "
                    f"expected {expected_type.__name__}"
                )

    # 8. Validate severity
    severity = metadata.get("severity")

    if isinstance(severity, dict):
        allowed_severities = {
            "critical",
            "high",
            "medium",
            "low",
            "unknown",
        }

        severity_value = severity.get("value")

        if (
            not isinstance(severity_value, str)
            or severity_value not in allowed_severities
        ):
            errors.append(
                f"Invalid severity value: {severity_value}"
            )

        # 9. Validate verification status
    verification = metadata.get("verification")

    if isinstance(verification, dict):
        allowed_verification_statuses = {
            "author_reported",
            "analyzed",
            "independently_reproduced",
        }

        verification_status = verification.get("status")

        if (
            not isinstance(verification_status, str)
            or verification_status not in allowed_verification_statuses
        ):
            errors.append(
                f"Invalid verification status: {verification_status}"
            )

        independently_reproduced = verification.get(
            "independently_reproduced"
        )

        if (
            verification_status in {"author_reported", "analyzed"}
            and independently_reproduced is True
        ):
            errors.append(
                "Inconsistent verification: "
                f"'{verification_status}' cannot have "
                "independently_reproduced=True"
            )

        elif (
            verification_status == "independently_reproduced"
            and independently_reproduced is not True
        ):
            errors.append(
                "Inconsistent verification: "
                "'independently_reproduced' requires "
                "independently_reproduced=True"
            )

    return errors

    # 10. Validate non-empty identifiers
    for field in ("id", "title"):
        if isinstance(metadata.get(field), str):
            if not metadata[field].strip():
                errors.append(f"Field '{field}' cannot be empty")

    return errors



def main():
    parser = argparse.ArgumentParser(
        description="Validate AI-OSF Markdown writeups."
    )
    parser.add_argument("file", type=Path, help="Writeup Markdown file")
    args = parser.parse_args()

    errors = validate_writeup(args.file)

    if errors:
        print(f"[FAIL] {args.file}")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print(f"[OK] Valid writeup: {args.file}")

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


if __name__ == "__main__":
    main()
