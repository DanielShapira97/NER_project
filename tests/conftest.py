from __future__ import annotations

from pathlib import Path

import pytest
from docx import Document

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def sample_docx_path() -> Path:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    path = FIXTURES / "sample.docx"
    if not path.exists():
        doc = Document()
        doc.add_paragraph("We use Python and Microsoft Azure for our data lake.")
        doc.save(path)
    return path


@pytest.fixture(scope="session")
def tech_model_path():
    root = Path(__file__).resolve().parents[1] / "models" / "complex-ner"
    for name in ("model-best", "model-last"):
        candidate = root / name
        if candidate.exists():
            return candidate
    if root.exists() and (root / "meta.json").exists():
        return root
    pytest.skip("Custom NER model not trained; run scripts/train_complex_ner.py")
