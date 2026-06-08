"""Merge custom tech NER spans with pretrained ORG/PERSON/PRODUCT."""

from __future__ import annotations

from dataclasses import dataclass

from files_translator.ner.labels import TECH_EXCLUDED_LABELS


@dataclass(frozen=True)
class EntitySpan:
    text: str
    label: str
    source: str
    start_char: int
    end_char: int


def _overlap_ratio(a_start: int, a_end: int, b_start: int, b_end: int) -> float:
    overlap = max(0, min(a_end, b_end) - max(a_start, b_start))
    if overlap == 0:
        return 0.0
    a_len = a_end - a_start
    b_len = b_end - b_start
    shorter = min(a_len, b_len)
    return overlap / shorter if shorter else 0.0


def _prefer_tech_over_pretrained(tech: EntitySpan, pre: EntitySpan) -> bool:
    if tech.label in TECH_EXCLUDED_LABELS:
        return False
    return _overlap_ratio(tech.start_char, tech.end_char, pre.start_char, pre.end_char) >= 0.5


def merge_entities(
    tech_spans: list[EntitySpan],
    pretrained_spans: list[EntitySpan],
) -> list[EntitySpan]:
    """
    Combine tech and pretrained spans.

    When overlap >= 50% of the shorter span, prefer tech unless label is excluded.
    """
    tech_kept = [s for s in tech_spans if s.label not in TECH_EXCLUDED_LABELS]
    result = list(tech_kept)

    for pre in pretrained_spans:
        dominated = False
        for tech in tech_kept:
            if _prefer_tech_over_pretrained(tech, pre):
                dominated = True
                break
        if not dominated:
            result.append(pre)

    result.sort(key=lambda s: (s.start_char, s.end_char))
    return result
