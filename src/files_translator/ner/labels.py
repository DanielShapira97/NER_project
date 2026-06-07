"""Label allowlists for preserve-list extraction."""

PRETRAINED_PRESERVE_LABELS = frozenset({"ORG", "PERSON", "PRODUCT"})

# Raw labels from multilingual / Hebrew pipelines mapped to canonical output labels.
PRETRAINED_LABEL_ALIASES: dict[str, str] = {
    "PER": "PERSON",
    "PERS": "PERSON",
    "MISC": "PRODUCT",
}

# Stack Overflow usernames are noisy in business documents.
TECH_EXCLUDED_LABELS = frozenset({"User_Name"})
