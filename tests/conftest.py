from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cdek.client import CdekClient  # noqa: E402


@pytest.fixture(scope="session")
def test_client() -> CdekClient:
    """Фикстура клиента в тестовом режиме CDEK."""
    return CdekClient("TEST")
