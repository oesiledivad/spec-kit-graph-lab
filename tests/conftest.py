"""Configuración compartida de pytest para graphcli."""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
DATA = ROOT / "data"
FIXTURES = Path(__file__).resolve().parent / "fixtures"

# Permite importar graphcli en las pruebas unitarias sin instalar el paquete.
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@dataclass
class CliResult:
    returncode: int
    stdout: str
    stderr: str


def run_cli(*args: str | Path) -> CliResult:
    """Ejecuta `python -m graphcli ...` como lo haría el usuario."""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, "-m", "graphcli", *map(str, args)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=ROOT,
        env=env,
    )
    return CliResult(proc.returncode, proc.stdout, proc.stderr)


@pytest.fixture
def cli():
    return run_cli
