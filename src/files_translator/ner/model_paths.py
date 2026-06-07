"""Resolve trained model directories."""

from __future__ import annotations

from pathlib import Path


def resolve_tech_model_path(base_path: str | Path) -> Path:
    """Prefer model-best, then model-last, then directory with meta.json."""
    root = Path(base_path)
    for name in ("model-best", "model-last"):
        candidate = root / name
        if (candidate / "meta.json").exists():
            return candidate
    if (root / "meta.json").exists():
        return root
    raise FileNotFoundError(
        f"No tech NER model at {base_path}. Train with scripts/train_stackoverflow_ner.py."
    )
