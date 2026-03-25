import re


def clean_text(text):
    """
    Basic cleaning:
    - lowercase
    - remove punctuation
    - remove extra spaces
    """

    text = text.lower()

    # remove special characters
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def tokenize(text):
    """
    Split sentence into words
    """
    return text.split()


def remove_stopwords(tokens):
    """
    Remove common useless words
    """

    stopwords = {
        "the", "is", "in", "at", "of", "on", "and",
        "a", "to", "for", "with", "by"
    }

    return [word for word in tokens if word not in stopwords]


def preprocess_log_message(message):
    """
    Full preprocessing pipeline
    """

    cleaned = clean_text(message)

    tokens = tokenize(cleaned)

    filtered_tokens = remove_stopwords(tokens)

    return " ".join(filtered_tokens)