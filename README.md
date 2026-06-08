# Files Translator

Step 1: extract a **preserve list** (terms that should not be translated) from uploaded `.docx` files using hybrid spaCy NER.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
python -m spacy download en_core_web_sm
python -m spacy download xx_ent_wiki_sm
```

`xx_ent_wiki_sm` is the multilingual NER fallback for Hebrew (`he_core_news_sm` is not published for spaCy 3.8). Override with `SPACY_HE_MODEL` if you install another Hebrew pipeline (e.g. `he_ner_news_trf`).

## Train custom NER (MorryShah/complex_ner)

Dataset: [MorryShah/complex_ner](https://huggingface.co/datasets/MorryShah/complex_ner) — business, legal, and software entities.

```bash
python scripts/convert_hf_to_spacy.py
python scripts/train_complex_ner.py
```

Outputs:

- `data/train.spacy`, `data/dev.spacy` — converted dataset
- `models/complex-ner/` — trained model

Set `TECH_NER_MODEL_PATH=models/complex-ner` (default) before running the API or CLI.

## CLI

```bash
python -m files_translator.cli --input document.docx --output preserve.json
```

## API

```bash
uvicorn app.main:app --reload
```

`POST /preserve-list` with multipart field `file` (`.docx` only).

Environment variables (optional):

| Variable | Default |
|----------|---------|
| `TECH_NER_MODEL_PATH` | `models/complex-ner` |
| `SPACY_EN_MODEL` | `en_core_web_sm` |
| `SPACY_HE_MODEL` | `xx_ent_wiki_sm` |

## JSON response

```json
{
  "source_filename": "report.docx",
  "paragraph_count": 12,
  "preserve_terms": [
    {
      "text": "GenTech Solutions",
      "label": "ORGANIZATION",
      "source": "complex-ner",
      "occurrences": [{"paragraph_index": 0, "start_char": 7, "end_char": 22}]
    }
  ]
}
```

## Limitations (this milestone)

- Paragraph text only (no tables, headers/footers, or text boxes).
- Custom NER is English-trained on complex_ner; Hebrew docs use `xx_ent_wiki_sm` (or `SPACY_HE_MODEL`) for ORG/PERSON/PRODUCT.
- Translation, RTL, and design preservation are not implemented yet.
