"""Convert token-level BIO tags to character spans."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BioEntity:
    label: str
    start_char: int
    end_char: int
    text: str


def _token_spans(tokens: list[str]) -> list[tuple[int, int]]:
    """Map tokens to character spans (space-separated, no trailing space after last token)."""
    spans: list[tuple[int, int]] = []
    pos = 0
    for i, token in enumerate(tokens):
        start = pos
        end = pos + len(token)
        spans.append((start, end))
        pos = end + (1 if i < len(tokens) - 1 else 0)
    return spans


def bio_tags_to_entities(tokens: list[str], tags: list[str]) -> list[BioEntity]:
    """
    Convert aligned tokens and BIO string tags to entity spans.

    Tags use format B-Label, I-Label, or O.
    """
    if len(tokens) != len(tags):
        raise ValueError(f"tokens length {len(tokens)} != tags length {len(tags)}")

    char_spans = _token_spans(tokens)
    entities: list[BioEntity] = []
    current_label: str | None = None
    start_idx = 0

    def flush(end_idx: int) -> None:
        nonlocal current_label, start_idx
        if current_label is None:
            return
        start_char = char_spans[start_idx][0]
        end_char = char_spans[end_idx][1]
        text = " ".join(tokens[start_idx : end_idx + 1])
        entities.append(
            BioEntity(
                label=current_label,
                start_char=start_char,
                end_char=end_char,
                text=text,
            )
        )
        current_label = None

    for i, tag in enumerate(tags):
        if tag == "O" or not tag:
            flush(i - 1)
            continue

        if "-" not in tag:
            raise ValueError(f"Invalid BIO tag: {tag!r}")

        prefix, label = tag.split("-", 1)
        if prefix == "B":
            flush(i - 1)
            current_label = label
            start_idx = i
        elif prefix == "I":
            if current_label is None:
                current_label = label
                start_idx = i
            elif current_label != label:
                flush(i - 1)
                current_label = label
                start_idx = i
        else:
            raise ValueError(f"Invalid BIO prefix in tag: {tag!r}")

    flush(len(tokens) - 1)
    return entities
