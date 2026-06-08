#!/usr/bin/env python3
"""Train custom complex_ner model and write models/complex-ner/."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs" / "complex_ner.cfg"
TRAIN_DATA = ROOT / "data" / "train.spacy"
OUTPUT_DIR = ROOT / "models" / "complex-ner"


def main() -> None:
    if not TRAIN_DATA.exists():
        print("Missing data/train.spacy — run scripts/convert_hf_to_spacy.py first.", file=sys.stderr)
        sys.exit(1)

    OUTPUT_DIR.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        "-m",
        "spacy",
        "train",
        str(CONFIG),
        "--output",
        str(OUTPUT_DIR),
        "--paths.train",
        str(TRAIN_DATA),
        "--paths.dev",
        str(ROOT / "data" / "dev.spacy"),
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT / "configs", check=True)

    best = OUTPUT_DIR / "model-best"
    model_last = OUTPUT_DIR / "model-last"
    if best.exists():
        print(f"Training complete. Best model: {best}")
    elif model_last.exists():
        print(f"Training complete. Latest model: {model_last}")
    else:
        print(f"Training finished; check {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
