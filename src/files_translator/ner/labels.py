"""Label allowlists for preserve-list extraction."""

PRETRAINED_PRESERVE_LABELS = frozenset({"ORG", "PERSON", "PRODUCT"})

# Raw labels from multilingual / Hebrew pipelines mapped to canonical output labels.
PRETRAINED_LABEL_ALIASES: dict[str, str] = {
    "PER": "PERSON",
    "PERS": "PERSON",
    "MISC": "PRODUCT",
}

# complex_ner labels excluded from the preserve list (PII/temporal/noise for translation).
TECH_EXCLUDED_LABELS = frozenset({
    "USERNAME",
    "TEMPORAL_TIME_DATE",
    "ADDRESS",
    "ID_NUMBER",
    "CONTACT_INFO",
    "PASSWORD_OR_KEY",
    "BANK_OR_FINANCIAL_ACCOUNT",
    "HEALTH",
    "DEVICE_ID",
    "CRIMINAL",
    "RACIAL_ETHNIC",
    "POLITICAL",
    "RELIGIOUS",
    "SEXUAL_ORIENTATION",
    "BEHAVIORAL",
    "SERVER_IP_ADDRESS",
    "FINANCIAL",
    "NUMBER",
    "CURRENCY",
    "COMMUNICATION",
})
