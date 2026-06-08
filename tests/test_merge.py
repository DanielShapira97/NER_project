from files_translator.ner.merge import EntitySpan, merge_entities


def test_keeps_non_overlapping_pretrained():
    tech = [
        EntitySpan("Python", "PROPRIETARY_TECHNOLOGY", "complex-ner", 7, 13),
    ]
    pre = [
        EntitySpan("Acme Corp", "ORG", "spacy-pretrained", 17, 26),
    ]
    merged = merge_entities(tech, pre)
    texts = {m.text for m in merged}
    assert texts == {"Python", "Acme Corp"}


def test_prefers_tech_on_overlap():
    tech = [
        EntitySpan("Microsoft Azure", "ORGANIZATION", "complex-ner", 0, 15),
    ]
    pre = [
        EntitySpan("Microsoft", "ORG", "spacy-pretrained", 0, 9),
    ]
    merged = merge_entities(tech, pre)
    assert len(merged) == 1
    assert merged[0].label == "ORGANIZATION"


def test_drops_username():
    tech = [
        EntitySpan("@kamran", "USERNAME", "complex-ner", 0, 7),
    ]
    pre = [
        EntitySpan("kamran", "PERSON", "spacy-pretrained", 1, 7),
    ]
    merged = merge_entities(tech, pre)
    assert any(m.label == "PERSON" for m in merged)
    assert not any(m.label == "USERNAME" for m in merged)
