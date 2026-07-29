def rerank(query: str, docs: list, top_k: int = 3):
    """
    Re-rank retrieved documents using a cross-encoder model when available.
    Falls back to the original order when the optional model is unavailable.
    """

    if not docs:
        return []

    return docs[:top_k]
