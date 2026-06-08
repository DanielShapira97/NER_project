#!/usr/bin/env python3
"""Convert MorryShah/complex_ner from Hugging Face to spaCy DocBin files."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from datasets import load_dataset  # noqa: E402
import spacy  # noqa: E402
from spacy.tokens import DocBin  # noqa: E402
from spacy.util import filter_spans  # noqa: E402
from tqdm import tqdm  # noqa: E402

from files_translator.ner.entity_spans import entities_to_spans  # noqa: E402

DATASET_ID = "MorryShah/complex_ner"
DATA_DIR = ROOT / "data"
TRAIN_OUT = DATA_DIR / "train.spacy"
DEV_OUT = DATA_DIR / "dev.spacy"


def row_to_doc(nlp: spacy.language.Language, text: str, entities: list[dict]):
    doc = nlp.make_doc(text)
    spans = []
    for ent in entities_to_spans(text, entities):
        span = doc.char_span(
            ent.start_char,
            ent.end_char,
            label=ent.label,
            alignment_mode="expand",
        )
        if span is not None:
            spans.append(span)
    doc.set_ents(filter_spans(spans))
    return doc


def convert_split(nlp, dataset_split) -> DocBin:
    db = DocBin(store_user_data=False)
    skipped = 0
    for row in tqdm(dataset_split, desc="Converting"):
        text = row["text"]
        entities = row["entities"]
        doc = row_to_doc(nlp, text, entities)
        if not doc.ents and entities:
            skipped += 1
        db.add(doc)
    if skipped:
        print(f"Warning: {skipped} rows had entities but no aligned spans")
    return db


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Loading {DATASET_ID} ...")
    ds = load_dataset(DATASET_ID)

    nlp = spacy.blank("en")

    print("Converting train split ...")
    train_db = convert_split(nlp, ds["train"])
    train_db.to_disk(TRAIN_OUT)
    print(f"Wrote {TRAIN_OUT}")

    print("Converting test split (dev) ...")
    dev_db = convert_split(nlp, ds["test"])
    dev_db.to_disk(DEV_OUT)
    print(f"Wrote {DEV_OUT}")


if __name__ == "__main__":
    main()
