from files_translator.ner.merge import EntitySpan, merge_entities


def test_keeps_non_overlapping_pretrained():
    tech = [
        EntitySpan("Python", "Language", "stackoverflow-ner", 7, 13),
    ]
    pre = [
        EntitySpan("Acme Corp", "ORG", "spacy-pretrained", 17, 26),
    ]
    merged = merge_entities(tech, pre)
    texts = {m.text for m in merged}
    assert texts == {"Python", "Acme Corp"}


def test_prefers_tech_on_overlap():
    tech = [
        EntitySpan("SQL Fiddle", "Application", "stackoverflow-ner", 0, 10),
    ]
    pre = [
        EntitySpan("SQL", "ORG", "spacy-pretrained", 0, 3),
    ]
    merged = merge_entities(tech, pre)
    assert len(merged) == 1
    assert merged[0].label == "Application"


def test_drops_user_name():
    tech = [
        EntitySpan("@KamranFarzami", "User_Name", "stackoverflow-ner", 0, 15),
    ]
    pre = [
        EntitySpan("KamranFarzami", "PERSON", "spacy-pretrained", 1, 14),
    ]
    merged = merge_entities(tech, pre)
    assert any(m.label == "PERSON" for m in merged)
    assert not any(m.label == "User_Name" for m in merged)
