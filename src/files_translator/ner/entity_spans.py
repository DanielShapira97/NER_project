"""Locate character spans for entity dicts inside document text."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TextEntity:
    label: str
    start_char: int
    end_char: int
    text: str


def _overlaps(start: int, end: int, used: list[tuple[int, int]]) -> bool:
    for used_start, used_end in used:
        if start < used_end and end > used_start:
            return True
    return False


def entities_to_spans(text: str, entities: list[dict]) -> list[TextEntity]:
    """
    Map {"text": "...", "type": "..."} items to non-overlapping char spans in text.

    When the same surface form appears multiple times, the next unused match is used.
    """
    used_ranges: list[tuple[int, int]] = []
    spans: list[TextEntity] = []

    for ent in entities:
        needle = ent.get("text", "")
        label = ent.get("type", "")
        if not needle or not label:
            continue

        pos = 0
        matched = False
        while pos <= len(text) - len(needle):
            idx = text.find(needle, pos)
            if idx == -1:
                break
            end = idx + len(needle)
            if not _overlaps(idx, end, used_ranges):
                spans.append(
                    TextEntity(
                        label=label,
                        start_char=idx,
                        end_char=end,
                        text=needle,
                    )
                )
                used_ranges.append((idx, end))
                matched = True
                break
            pos = idx + 1

        if not matched:
            continue

    spans.sort(key=lambda s: (s.start_char, s.end_char))
    return spans
