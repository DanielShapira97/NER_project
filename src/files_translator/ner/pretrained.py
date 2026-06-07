"""Pretrained spaCy en/he models for ORG, PERSON, PRODUCT."""

from __future__ import annotations

import spacy
from spacy.language import Language

from files_translator.ner.labels import PRETRAINED_LABEL_ALIASES, PRETRAINED_PRESERVE_LABELS
from files_translator.ner.merge import EntitySpan


def load_pretrained_models(
    en_model: str = "en_core_web_sm",
    he_model: str = "xx_ent_wiki_sm",
) -> dict[str, Language]:
    return {
        "en": spacy.load(en_model),
        "he": spacy.load(he_model),
    }


def _canonical_label(label: str) -> str | None:
    if label in PRETRAINED_PRESERVE_LABELS:
        return label
    return PRETRAINED_LABEL_ALIASES.get(label)


def extract_pretrained_entities(nlp: Language, text: str) -> list[EntitySpan]:
    doc = nlp(text)
    spans: list[EntitySpan] = []
    for ent in doc.ents:
        label = _canonical_label(ent.label_)
        if label is None:
            continue
        spans.append(
            EntitySpan(
                text=ent.text,
                label=label,
                source="spacy-pretrained",
                start_char=ent.start_char,
                end_char=ent.end_char,
            )
        )
    return spans
