#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path

from tools.writeup_parser import WriteupDocument, parse_writeup
from tools.finding_extractor import Finding, extract_finding
from core.classification_engine import (
    ClassificationResult,
    classify_finding,
)


@dataclass
class PipelineResult:
    document: WriteupDocument
    finding: Finding
    classification: ClassificationResult


def process_writeup(path: Path) -> PipelineResult:
    """
    Process a Markdown writeup through the AI-OSF pipeline.

    Parsing, extraction and classification remain separate
    operations coordinated by this module.
    """

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
