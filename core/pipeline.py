#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path

from tools.writeup_parser import WriteupDocument, parse_writeup
from tools.writeup_validator import validate_writeup
from tools.finding_extractor import Finding, extract_finding
from core.classification_engine import (
    ClassificationResult,
    classify_finding,
)


class WriteupValidationError(Exception):
    """Raised when a writeup fails schema validation."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        message = "Writeup validation failed:\n" + "\n".join(
            f"  - {error}" for error in errors
        )
        super().__init__(message)


@dataclass
class PipelineResult:
    document: WriteupDocument
    finding: Finding
    classification: ClassificationResult


def process_writeup(path: Path) -> PipelineResult:
    """
    Process a Markdown writeup through the AI-OSF pipeline.

    Validates the writeup before parsing, extraction and
    classification.
    """

    errors = validate_writeup(path)

    if errors:
        raise WriteupValidationError(errors)

    document = parse_writeup(path)

    finding = extract_finding(document)

    classification = classify_finding(
        finding,
        document.metadata.get("classification"),
    )

    return PipelineResult(
        document=document,
        finding=finding,
        classification=classification,
    )
