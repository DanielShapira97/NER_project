from files_translator.ner.bio import bio_tags_to_entities


def test_sql_fiddle_application():
    tokens = ["SQL", "Fiddle", ":", "http://sqlfiddle.com/#!9/11093"]
    tags = ["B-Application", "I-Application", "O", "O"]
    entities = bio_tags_to_entities(tokens, tags)
    assert len(entities) == 1
    assert entities[0].label == "Application"
    assert entities[0].text == "SQL Fiddle"


def test_csharp_dotnet_language_library():
    tokens = ["I", "have", "a", "C#", "/.NET", "application"]
    tags = ["O", "O", "O", "B-Language", "B-Library", "O"]
    entities = bio_tags_to_entities(tokens, tags)
    labels = {e.label: e.text for e in entities}
    assert labels["Language"] == "C#"
    assert labels["Library"] == "/.NET"


def test_tables_data_structure():
    tokens = ["If", "I", "would", "have", "2", "tables"]
    tags = ["O", "O", "O", "O", "O", "B-Data_Structure"]
    entities = bio_tags_to_entities(tokens, tags)
    assert len(entities) == 1
    assert entities[0].label == "Data_Structure"
    assert entities[0].text == "tables"
