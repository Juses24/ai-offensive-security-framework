import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

WRITEUP_PATH = (
    PROJECT_ROOT
    / "knowledge/writeups/hackerone/nextcloud-out-of-office-bola.md"
)


def test_cli_processes_writeup_successfully():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.ai_osf",
            "process",
            str(WRITEUP_PATH),
        ],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    assert result.returncode == 0
    assert "Writeup processed successfully." in result.stdout
    assert "Nextcloud Out-of-Office API BOLA" in result.stdout
    assert "Broken Object Level Authorization" in result.stdout
    assert "author_reported" in result.stdout


def test_cli_handles_missing_writeup():
    missing_path = PROJECT_ROOT / "nonexistent-writeup.md"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.ai_osf",
            "process",
            str(missing_path),
        ],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    assert result.returncode == 1
    assert "[ERROR]" in result.stdout
