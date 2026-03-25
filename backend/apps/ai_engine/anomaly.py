from sklearn.ensemble import IsolationForest


def detect_anomalies(vectors):
    """
    Detect anomalies using Isolation Forest
    """

    model = IsolationForest(contamination=0.1, random_state=42)

    predictions = model.fit_predict(vectors)

    # Convert:
    # -1 → anomaly
    #  1 → normal
    anomalies = [1 if p == -1 else 0 for p in predictions]

    return anomalies, model