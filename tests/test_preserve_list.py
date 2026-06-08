import pytest

spacy = pytest.importorskip("spacy")


@pytest.fixture(scope="module")
def pretrained_models():
    try:
        nlp_en = spacy.load("en_core_web_sm")
    except OSError:
        pytest.skip("en_core_web_sm not installed")
    try:
        nlp_he = spacy.load("xx_ent_wiki_sm")
    except OSError:
        pytest.skip("xx_ent_wiki_sm not installed")
    return nlp_en, nlp_he


def test_preserve_list_smoke(sample_docx_path, tech_model_path, pretrained_models):
    from files_translator.ner.tech import load_tech_model
    from files_translator.preserve_list import PreserveListBuilder

    nlp_en, nlp_he = pretrained_models
    builder = PreserveListBuilder(
        nlp_tech=load_tech_model(tech_model_path),
        nlp_en=nlp_en,
        nlp_he=nlp_he,
    )
    result = builder.build_from_docx(sample_docx_path)

    assert result["paragraph_count"] >= 1
    terms = {(t["text"], t["label"]) for t in result["preserve_terms"]}
    texts = {t[0] for t in terms}
    labels = {t[1] for t in terms}

    assert "Python" in texts or any("Python" in t for t in texts)
    assert len(result["preserve_terms"]) >= 2
    assert (
        "ORG" in labels
        or "ORGANIZATION" in labels
        or "PROPRIETARY_TECHNOLOGY" in labels
        or "CODE_RELATED" in labels
    )
