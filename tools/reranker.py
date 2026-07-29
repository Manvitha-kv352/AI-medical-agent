from sentence_transformers import CrossEncoder

# Load once when the application starts
reranker = CrossEncoder("BAAI/bge-reranker-base")


def rerank(query: str, docs: list, top_k: int = 3):
    """
    Re-rank retrieved documents using a cross-encoder model.
    """

    if not docs:
        return []

    pairs = [
        (query, doc["text"])
        for doc in docs
    ]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(scores, docs),
        key=lambda x: x[0],
        reverse=True
    )

    return [doc for _, doc in ranked[:top_k]]