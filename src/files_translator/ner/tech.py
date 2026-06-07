"""Custom stackoverflow-ner spaCy model."""

from __future__ import annotations

from pathlib import Path

import spacy
from spacy.language import Language

from files_translator.ner.merge import EntitySpan


def load_tech_model(model_path: str | Path) -> Language:
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Tech NER model not found at {path}. "
            "Run scripts/convert_hf_to_spacy.py and scripts/train_stackoverflow_ner.py first."
        )
    return spacy.load(path)


def extract_tech_entities(nlp: Language, text: str) -> list[EntitySpan]:
    doc = nlp(text)
    return [
        EntitySpan(
            text=ent.text,
            label=ent.label_,
            source="stackoverflow-ner",
            start_char=ent.start_char,
            end_char=ent.end_char,
        )
        for ent in doc.ents
    ]
