"""CLI for preserve-list extraction."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract preserve list from a DOCX file.")
    parser.add_argument("--input", "-i", required=True, help="Path to .docx file")
    parser.add_argument("--output", "-o", help="Write JSON here (default: stdout)")
    parser.add_argument(
        "--tech-model",
        default=os.environ.get("TECH_NER_MODEL_PATH", "models/complex-ner"),
    )
    parser.add_argument(
        "--en-model",
        default=os.environ.get("SPACY_EN_MODEL", "en_core_web_sm"),
    )
    parser.add_argument(
        "--he-model",
        default=os.environ.get("SPACY_HE_MODEL", "xx_ent_wiki_sm"),
    )
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if input_path.suffix.lower() != ".docx":
        print("Error: input must be a .docx file", file=sys.stderr)
        return 1

    from files_translator.preserve_list import load_builder

    builder = load_builder(
        tech_model_path=args.tech_model,
        en_model=args.en_model,
        he_model=args.he_model,
    )
    result = builder.build_from_docx(input_path, source_filename=input_path.name)
    payload = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
