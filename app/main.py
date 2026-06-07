"""FastAPI service for preserve-list extraction."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from files_translator.preserve_list import PreserveListBuilder, load_builder

_builder: PreserveListBuilder | None = None


def _get_builder() -> PreserveListBuilder:
    if _builder is None:
        raise HTTPException(
            status_code=500,
            detail=(
                "Models not loaded. Set TECH_NER_MODEL_PATH and ensure "
                "en_core_web_sm and SPACY_HE_MODEL (default xx_ent_wiki_sm) are installed."
            ),
        )
    return _builder


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _builder
    tech_path = os.environ.get("TECH_NER_MODEL_PATH", "models/stackoverflow-ner")
    en_model = os.environ.get("SPACY_EN_MODEL", "en_core_web_sm")
    he_model = os.environ.get("SPACY_HE_MODEL", "xx_ent_wiki_sm")

    _builder = load_builder(tech_model_path=tech_path, en_model=en_model, he_model=he_model)
    yield
    _builder = None


app = FastAPI(
    title="Files Translator",
    description="Extract preserve-list JSON from DOCX uploads.",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/preserve-list")
async def preserve_list(file: UploadFile = File(...)) -> JSONResponse:
    filename = file.filename or "upload.docx"
    if not filename.lower().endswith(".docx"):
        raise HTTPException(status_code=422, detail="Only .docx files are supported.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=422, detail="Empty file.")

    try:
        builder = _get_builder()
        result: dict[str, Any] = builder.build_from_docx(
            content,
            source_filename=filename,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return JSONResponse(content=result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
