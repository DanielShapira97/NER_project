#!/usr/bin/env python3
"""Convert mrm8488/stackoverflow-ner from Hugging Face to spaCy DocBin files."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from datasets import load_dataset  # noqa: E402
import spacy  # noqa: E402
from spacy.tokens import DocBin  # noqa: E402
from tqdm import tqdm  # noqa: E402

from files_translator.ner.bio import bio_tags_to_entities  # noqa: E402

DATA_DIR = ROOT / "data"
TRAIN_OUT = DATA_DIR / "train.spacy"
DEV_OUT = DATA_DIR / "dev.spacy"


def row_to_doc(nlp: spacy.language.Language, tokens: list[str], tags: list[str]):
    text = " ".join(tokens)
    doc = nlp.make_doc(text)
    ents = []
    for ent in bio_tags_to_entities(tokens, tags):
        span = doc.char_span(ent.start_char, ent.end_char, label=ent.label, alignment_mode="expand")
        if span is not None:
            ents.append(span)
    doc.set_ents(ents)
    return doc


def convert_split(nlp, dataset_split) -> DocBin:
    db = DocBin(store_user_data=False)
    skipped = 0
    for row in tqdm(dataset_split, desc="Converting"):
        tokens = row["tokens"]
        tags = row["ner_tags"]
        doc = row_to_doc(nlp, tokens, tags)
        if not doc.ents and any(t != "O" for t in tags):
            skipped += 1
        db.add(doc)
    if skipped:
        print(f"Warning: {skipped} rows had tags but no aligned spans")
    return db


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("Loading mrm8488/stackoverflow-ner ...")
    ds = load_dataset("mrm8488/stackoverflow-ner")

    nlp = spacy.blank("en")

    print("Converting train split ...")
    train_db = convert_split(nlp, ds["train"])
    train_db.to_disk(TRAIN_OUT)
    print(f"Wrote {TRAIN_OUT}")

    print("Converting validation split ...")
    dev_db = convert_split(nlp, ds["validation"])
    dev_db.to_disk(DEV_OUT)
    print(f"Wrote {DEV_OUT}")


if __name__ == "__main__":
    main()
