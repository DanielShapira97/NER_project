"""Simple English / Hebrew language detection for NER routing."""

from __future__ import annotations

from langdetect import DetectorFactory, LangDetectException, detect

DetectorFactory.seed = 0

SUPPORTED_LANGS = frozenset({"en", "he"})


def detect_language(text: str, default: str = "en") -> str:
    """Detect en or he; fall back to default on failure or unsupported language."""
    sample = text.strip()
    if not sample:
        return default
    try:
        code = detect(sample)
    except LangDetectException:
        return default
    if code == "iw":
        return "he"
    if code in SUPPORTED_LANGS:
        return code
    return default


def detect_document_language(paragraphs: list[str], default: str = "en") -> str:
    """Use the first substantial paragraph, then majority vote on first five."""
    substantial = [p for p in paragraphs if len(p.strip()) >= 20]
    samples = substantial[:5] if substantial else paragraphs[:5]
    if not samples:
        return default
    votes: dict[str, int] = {}
    for sample in samples:
        lang = detect_language(sample, default=default)
        votes[lang] = votes.get(lang, 0) + 1
    return max(votes, key=votes.get)
