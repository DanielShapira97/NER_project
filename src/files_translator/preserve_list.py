"""Build preserve-list JSON from DOCX input."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, Union

from spacy.language import Language

from files_translator.docx_text import ParagraphText, extract_paragraphs
from files_translator.language import detect_document_language
from files_translator.ner.merge import EntitySpan, merge_entities
from files_translator.ner.pretrained import extract_pretrained_entities
from files_translator.ner.tech import extract_tech_entities


@dataclass
class PreserveListBuilder:
    nlp_tech: Language
    nlp_en: Language
    nlp_he: Language

    def build_from_docx(
        self,
        source: Union[str, Path, BinaryIO, bytes],
        source_filename: str | None = None,
    ) -> dict[str, Any]:
        paragraphs = extract_paragraphs(source)
        texts = [p.text for p in paragraphs]
        doc_lang = detect_document_language(texts)
        nlp_pre = self.nlp_he if doc_lang == "he" else self.nlp_en

        aggregated: dict[tuple[str, str, str], dict[str, Any]] = {}

        for para in paragraphs:
            tech = extract_tech_entities(self.nlp_tech, para.text)
            pre = extract_pretrained_entities(nlp_pre, para.text)
            merged = merge_entities(tech, pre)

            for span in merged:
                key = (_normalize_key(span.text), span.label, span.source)
                if key not in aggregated:
                    aggregated[key] = {
                        "text": span.text,
                        "label": span.label,
                        "source": span.source,
                        "occurrences": [],
                    }
                aggregated[key]["occurrences"].append(
                    {
                        "paragraph_index": para.index,
                        "start_char": span.start_char,
                        "end_char": span.end_char,
                    }
                )

        preserve_terms = sorted(
            aggregated.values(),
            key=lambda item: (
                item["occurrences"][0]["paragraph_index"],
                item["occurrences"][0]["start_char"],
            ),
        )

        filename = source_filename
        if filename is None and isinstance(source, (str, Path)):
            filename = Path(source).name

        return {
            "source_filename": filename or "upload.docx",
            "paragraph_count": len(paragraphs),
            "document_language": doc_lang,
            "preserve_terms": preserve_terms,
        }


def _normalize_key(text: str) -> str:
    if re.search(r"[A-Za-z]", text):
        return text.casefold()
    return text


def load_builder(
    tech_model_path: str | Path = "models/stackoverflow-ner",
    en_model: str = "en_core_web_sm",
    he_model: str = "xx_ent_wiki_sm",
) -> PreserveListBuilder:
    from files_translator.ner.model_paths import resolve_tech_model_path
    from files_translator.ner.pretrained import load_pretrained_models
    from files_translator.ner.tech import load_tech_model

    pretrained = load_pretrained_models(en_model=en_model, he_model=he_model)
    return PreserveListBuilder(
        nlp_tech=load_tech_model(resolve_tech_model_path(tech_model_path)),
        nlp_en=pretrained["en"],
        nlp_he=pretrained["he"],
    )
