from files_translator.ner.entity_spans import entities_to_spans


def test_entities_to_spans_basic():
    text = "We use Python at Acme Corp."
    entities = [
        {"text": "Python", "type": "PROPRIETARY_TECHNOLOGY"},
        {"text": "Acme Corp", "type": "ORGANIZATION"},
    ]
    spans = entities_to_spans(text, entities)
    assert len(spans) == 2
    by_label = {s.label: s.text for s in spans}
    assert by_label["PROPRIETARY_TECHNOLOGY"] == "Python"
    assert by_label["ORGANIZATION"] == "Acme Corp"


def test_entities_to_spans_avoids_overlap():
    text = "Azure Azure"
    entities = [
        {"text": "Azure", "type": "ORGANIZATION"},
        {"text": "Azure", "type": "ORGANIZATION"},
    ]
    spans = entities_to_spans(text, entities)
    assert len(spans) == 2
    assert spans[0].start_char == 0
    assert spans[1].start_char == 6
