from sklearn.cluster import KMeans


def cluster_logs(vectors, k=3):
    
    """
    Perform KMeans clustering
    """

    model = KMeans(n_clusters=k, random_state=42)

    labels = model.fit_predict(vectors)

    return labels, model