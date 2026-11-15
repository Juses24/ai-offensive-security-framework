# AI Offensive Security Framework (AI-OSF)

**An extensible framework for offensive security research, vulnerability analysis, and bug bounty intelligence.**

AI-OSF is an experimental Python-based framework designed to help penetration testers and security researchers organize vulnerability knowledge, process technical writeups, and build structured security intelligence.

The project is being developed incrementally, with an emphasis on deterministic processing, traceable results, modular architecture, and evidence-based vulnerability assessment.

## Project Objectives

- Support Web and API security research.
- Organize vulnerability intelligence and technical writeups.
- Extract structured findings from security reports.
- Map vulnerabilities to OWASP categories and CWE references.
- Identify relationships between vulnerability types.
- Build reusable security methodologies and research skills.
- Preserve the distinction between reported information and independently verified findings.
- Establish a foundation for future AI-assisted security analysis.

## Architecture

The current processing workflow follows four independent stages:

```text
Markdown Writeup
       |
       v
  Writeup Parser
       |
       v
 Finding Extractor
       |
       v
 Classification Engine
       |
       v
  Pipeline Result
       |
       v
     CLI
```

Each component has a specific responsibility:

| Component | Responsibility |
|---|---|
| Writeup Parser | Reads Markdown writeups, extracts YAML Front Matter and validates its structure. |
| Finding Extractor | Converts writeup information into structured security findings. |
| Classification Engine | Normalizes vulnerability labels and maps known vulnerabilities against the knowledge base. |
| Pipeline | Coordinates parsing, extraction, and classification. |
| CLI | Provides a command-line interface for processing writeups. |
| Writeup Validator | Checks writeup metadata, required fields, endpoints, severity, and verification information. |

## Project Structure

```text
ai-offensive-security-framework/
├── agents/
├── config/
├── core/
│   ├── classification_engine.py
│   └── pipeline.py
├── data/
├── integrations/
│   └── mcp/
├── knowledge/
│   ├── bug_bounty/
│   │   ├── api/
│   │   ├── authentication/
│   │   ├── authorization/
│   │   ├── business_logic/
│   │   └── web/
│   ├── cves/
│   ├── exploitation/
│   │   ├── chains/
│   │   └── payloads/
│   ├── methodologies/
│   ├── owasp/
│   ├── vulnerabilities/
│   │   ├── api/
│   │   └── web/
│   └── writeups/
│       ├── bugcrowd/
│       ├── hackerone/
│       ├── htb/
│       ├── personal_research/
│       └── WRITEUP_TEMPLATE.md
├── skills/
│   ├── api/
│   ├── authentication/
│   ├── authorization/
│   ├── web/
│   └── webapi/
├── tests/
│   ├── test_classification_engine.py
│   ├── test_cli.py
│   ├── test_finding_extractor.py
│   ├── test_pipeline.py
│   ├── test_writeup_parser.py
│   └── test_writeup_validator.py
├── tools/
│   ├── ai_osf.py
│   ├── finding_extractor.py
│   ├── writeup_parser.py
│   └── writeup_validator.py
├── .github/
│   └── workflows/
│       └── tests.yml
├── requirements.txt
└── README.md
```

## Implemented Features

### 1. Structured Writeup Processing

AI-OSF supports Markdown security writeups using YAML Front Matter.

The writeup structure captures information such as:

- Writeup ID and title.
- Source platform and target.
- Affected endpoints.
- Vulnerability classifications.
- OWASP and CWE references.
- Severity.
- Verification status.
- Technical evidence and impact.

### 2. Writeup Parser

The parser extracts structured metadata and Markdown content.

It also handles invalid YAML, missing Front Matter, duplicate YAML keys, missing files, and invalid UTF-8 input.

### 3. Finding Extractor

The extractor converts parsed writeups into structured findings.

It captures vulnerability labels, affected endpoints, severity, impact, evidence, verification status, confidence, and source references.

### 4. Classification Engine

The initial classification engine uses a deterministic, rule-based registry.

Current functionality includes:

- BOLA recognition.
- Vulnerability name normalization.
- OWASP and CWE knowledge-base mappings.
- Related vulnerability concepts.
- Preservation of original vulnerability labels.

The initial BOLA mapping associates the vulnerability with OWASP API1:2023 and CWE-639.

Importantly, IDOR is not automatically classified as BOLA.

Original report classifications are kept separate from AI-OSF knowledge-base suggestions. Suggested mappings are not presented as independently verified facts.

### 5. Processing Pipeline

The pipeline coordinates the following components:

```python
from pathlib import Path
from core.pipeline import process_writeup

result = process_writeup(
    Path("knowledge/writeups/hackerone/nextcloud-out-of-office-bola.md")
)
```

The result contains:

- The parsed writeup document.
- The extracted finding.
- The classification result.

### 6. Command-Line Interface

AI-OSF provides a CLI for processing security writeups.

Example:

```bash
python -m tools.ai_osf process \
knowledge/writeups/hackerone/nextcloud-out-of-office-bola.md
```

The CLI displays the extracted finding, original report classifications, AI-OSF knowledge-base mappings, and related concepts.

## Installation

Clone the repository:

```bash
git clone https://github.com/Juses24/ai-offensive-security-framework.git

cd ai-offensive-security-framework
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Linux / Kali Linux**

```bash
source .venv/bin/activate
```

**Windows**

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running Tests

Run the complete test suite:

```bash
python -m pytest -v
```

The current test suite covers:

- Writeup validation.
- YAML and Markdown parsing.
- Finding extraction.
- Vulnerability classification.
- Pipeline integration.
- CLI execution and error handling.

**Current development milestone: 31 passing tests.**

GitHub Actions is also configured to execute the automated test suite.

## Development Roadmap

| Component | Status |
|---|---|
| Initial project structure | Completed |
| Knowledge base foundation | In progress |
| Writeup template and validation | Implemented |
| Writeup parser | Implemented |
| Finding extractor | Implemented |
| Classification engine | Initial implementation |
| Processing pipeline | Implemented and tested |
| Command-line interface | Initial implementation |
| Intelligence Engine | Planned |
| Vulnerability relationship analysis | Planned |
| AI-assisted analysis | Planned |
| MCP integrations | Planned |
| Specialized security agents | Planned |

## Technology Stack

- Python
- PyYAML
- pytest
- Kali Linux
- Git and GitHub
- GitHub Actions

**Future integrations:** OpenAI API and Model Context Protocol (MCP).

These integrations are planned and are not required by the current processing pipeline.

## Responsible Use

AI-OSF is intended for:

- Authorized penetration testing.
- Security research.
- Educational environments and labs.
- Legitimate bug bounty programs.

All active security testing must remain within explicitly authorized scope.

Human approval and oversight are required for security testing activities. The framework must not be used to access systems or data without authorization.

## Project Status

**Active Development — Foundation and Processing Pipeline**

The current version establishes a deterministic foundation for structured security writeup processing and vulnerability classification.

Future development will focus on expanding the knowledge base, improving vulnerability intelligence, and progressively introducing AI-assisted capabilities.

## License

License to be defined.
