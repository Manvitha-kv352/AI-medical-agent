import requests
import xml.etree.ElementTree as ET
import chromadb
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

# =========================
# VECTOR DB
# =========================
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./medical_db")

collection = client.get_or_create_collection(
    "pubmed_research"
)


# =========================
# TOOL 1: PUBMED SEARCH
# =========================
def pubmed_search(query: str, top_k: int = 5):

    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        f"esearch.fcgi?db=pubmed&term={query}&retmax={top_k}"
    )

    res = requests.get(url)
    root = ET.fromstring(res.text)

    return [i.text for i in root.findall(".//Id")]


# =========================
# TOOL 2: FETCH ABSTRACTS
# =========================
def fetch_abstracts(ids):

    if not ids:
        return []

    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        f"efetch.fcgi?db=pubmed&id={','.join(ids)}&retmode=xml"
    )

    res = requests.get(url)
    root = ET.fromstring(res.text)

    docs = []

    for article in root.findall(".//PubmedArticle"):

        title = article.findtext(".//ArticleTitle")
        pmid = article.findtext(".//PMID")

        abstract_parts = article.findall(".//AbstractText")
        abstract = " ".join(
            [a.text for a in abstract_parts if a.text]
        )

        if abstract:
            docs.append(
                {
                    "text": f"{title}\n{abstract}",
                    "pmid": pmid,
                }
            )

    return docs


# =========================
# TOOL 3: VECTOR SEARCH
# =========================
def vector_search(query: str, top_k: int = 3):

    q_emb = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=top_k,
    )

    return results


# =========================
# TOOL 4: BM25 SEARCH
# =========================
def bm25_search(query: str, docs: list, top_k: int = 3):

    if not docs:
        return []

    corpus = [doc["text"].split() for doc in docs]

    bm25 = BM25Okapi(corpus)

    query_tokens = query.split()

    scores = bm25.get_scores(query_tokens)

    ranked_docs = sorted(
        zip(scores, docs),
        key=lambda x: x[0],
        reverse=True,
    )

    return [doc for _, doc in ranked_docs[:top_k]]


# =========================
# TOOL 5: HYBRID SEARCH
# =========================
def hybrid_search(query: str, docs: list, top_k: int = 3):
    """
    Hybrid Retrieval:
    - Dense Retrieval (ChromaDB)
    - Sparse Retrieval (BM25)
    - Removes duplicates while preserving metadata
    """

    vector_results = vector_search(query, top_k=top_k)

    vector_docs = []

    if (
        vector_results
        and vector_results.get("documents")
        and vector_results.get("metadatas")
    ):

        documents = vector_results["documents"][0]
        metadatas = vector_results["metadatas"][0]

        for text, metadata in zip(documents, metadatas):

            vector_docs.append(
                {
                    "text": text,
                    "pmid": metadata.get("pmid")
                }
            )

    bm25_docs = bm25_search(query, docs, top_k)

    combined = vector_docs + bm25_docs

    unique_docs = []
    seen = set()

    for doc in combined:

        if doc["text"] not in seen:
            unique_docs.append(doc)
            seen.add(doc["text"])

    return unique_docs

# =========================
# TOOL 6: STORE DOCUMENTS
# =========================
def store_docs(docs):

    embeddings = embedding_model.encode(
        [d["text"] for d in docs]
    ).tolist()

    # Demo version:
    # Clear existing documents before storing new ones.
    try:
        old = collection.get()

        if old["ids"]:
            collection.delete(ids=old["ids"])

    except Exception:
        pass

    for i, d in enumerate(docs):

        collection.add(
            ids=[str(i)],
            documents=[d["text"]],
            embeddings=[embeddings[i]],
            metadatas=[
                {
                    "pmid": d["pmid"]
                }
            ],
        )

    return True