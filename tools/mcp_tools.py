import re
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote
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


def build_pubmed_query(query: str) -> str:
    if not query:
        return ""

    q = query.strip()
    lowered = q.lower()
    clauses = []

    if any(token in lowered for token in ["ai", "artificial intelligence", "machine learning", "deep learning"]):
        clauses.append("(artificial intelligence[Title/Abstract] OR AI[Title/Abstract] OR machine learning[Title/Abstract] OR deep learning[Title/Abstract])")

    if any(token in lowered for token in ["neuroscience", "neurology", "neuro", "brain", "neuroimaging"]):
        clauses.append("(neuroscience[Title/Abstract] OR neurology[Title/Abstract] OR neuroimaging[Title/Abstract] OR brain[Title/Abstract])")

    if any(token in lowered for token in ["healthcare", "health care", "clinical", "medical"]):
        clauses.append("(healthcare[Title/Abstract] OR clinical[Title/Abstract] OR medical[Title/Abstract])")

    if not clauses:
        return q

    return " AND ".join(clauses)


# =========================
# TOOL 1: PUBMED SEARCH
# =========================
def pubmed_search(query: str, top_k: int = 5):
    pubmed_query = build_pubmed_query(query)
    print("[Retrieval] User query:", query)
    print("[Retrieval] Generated PubMed query:", pubmed_query or query)

    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        f"esearch.fcgi?db=pubmed&term={quote(pubmed_query or query)}&retmax={top_k}"
    )

    res = requests.get(url, timeout=30)
    res.raise_for_status()
    root = ET.fromstring(res.text)

    ids = [i.text for i in root.findall(".//Id")]
    print("[Retrieval] Retrieved PMIDs before reranking:", ids)
    return ids


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

        title = article.findtext(".//ArticleTitle") or ""
        pmid = article.findtext(".//PMID") or ""
        publication_date = (
            article.findtext(".//PubDate/Year")
            or article.findtext(".//PubDate/MedlineDate")
            or ""
        )

        authors = []
        for author in article.findall(".//Author"):
            first = author.findtext("ForeName") or ""
            last = author.findtext("LastName") or ""
            initials = author.findtext("Initials") or ""
            name = " ".join(part for part in [first, last, initials] if part)
            if name:
                authors.append(name)

        abstract_parts = article.findall(".//AbstractText")
        abstract = " ".join(
            [a.text for a in abstract_parts if a.text]
        )

        if abstract:
            docs.append(
                {
                    "text": f"{title}\n{abstract}",
                    "title": title,
                    "abstract": abstract,
                    "authors": authors,
                    "publication_date": publication_date,
                    "pmid": pmid,
                    "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
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


def _tokenize(text: str):
    return re.findall(r"[a-z0-9]+", (text or "").lower())


# =========================
# TOOL 4: BM25 SEARCH
# =========================
def bm25_search(query: str, docs: list, top_k: int = 3):

    if not docs:
        return []

    corpus = [_tokenize(doc["text"]) for doc in docs]

    bm25 = BM25Okapi(corpus)

    query_tokens = _tokenize(query)

    scores = bm25.get_scores(query_tokens)

    ranked_docs = sorted(
        zip(scores, docs),
        key=lambda x: x[0],
        reverse=True,
    )

    ranked = []
    for score, doc in ranked_docs[:top_k]:
        new_doc = dict(doc)
        new_doc["bm25_score"] = float(score)
        ranked.append(new_doc)

    return ranked


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

    vector_results = vector_search(query, top_k=max(top_k * 2, 8))

    vector_docs = []

    if (
        vector_results
        and vector_results.get("documents")
        and vector_results.get("metadatas")
    ):

        documents = vector_results["documents"][0]
        metadatas = vector_results["metadatas"][0]

        for rank, (text, metadata) in enumerate(zip(documents, metadatas)):
            doc = {
                "text": text,
                "pmid": metadata.get("pmid"),
                "title": metadata.get("title"),
                "abstract": metadata.get("abstract"),
                "authors": metadata.get("authors"),
                "publication_date": metadata.get("publication_date"),
                "pubmed_url": metadata.get("pubmed_url"),
            }
            doc["vector_rank"] = rank
            vector_docs.append(doc)

    bm25_docs = bm25_search(query, docs, top_k=max(top_k * 2, 8))

    combined = {}
    for idx, doc in enumerate(vector_docs):
        key = doc.get("pmid") or doc.get("text")
        combined[key] = dict(doc)
        combined[key]["hybrid_score"] = 0.7 * (1 - (idx / max(1, len(vector_docs))))

    for doc in bm25_docs:
        key = doc.get("pmid") or doc.get("text")
        if key not in combined:
            combined[key] = dict(doc)
            combined[key]["hybrid_score"] = 0.0
        combined[key]["hybrid_score"] += 0.3 * max(0.0, min(1.0, doc.get("bm25_score", 0.0)))
        combined[key]["bm25_score"] = doc.get("bm25_score", 0.0)

    ranked_docs = sorted(
        combined.values(),
        key=lambda item: item.get("hybrid_score", 0.0),
        reverse=True,
    )

    return ranked_docs[:top_k]

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
                    "pmid": d.get("pmid", ""),
                    "title": d.get("title", ""),
                    "abstract": d.get("abstract", ""),
                    "authors": ", ".join(d.get("authors", [])),
                    "publication_date": d.get("publication_date", ""),
                    "pubmed_url": d.get("pubmed_url", ""),
                }
            ],
        )

    return True