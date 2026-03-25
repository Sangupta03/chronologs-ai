from sklearn.feature_extraction.text import TfidfVectorizer

from .preprocessing import preprocess_log_message


def vectorize_logs(messages):
    """
    Convert log messages into TF-IDF vectors
    """

    # Step 1: preprocess all messages
    processed_messages = [
        preprocess_log_message(msg) for msg in messages
    ]

    # Step 2: create vectorizer
    vectorizer = TfidfVectorizer()

    # Step 3: fit and transform
    vectors = vectorizer.fit_transform(processed_messages)

    return vectors, vectorizer