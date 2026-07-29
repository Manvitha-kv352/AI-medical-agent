import re
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote


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

    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        f"esearch.fcgi?db=pubmed&term={quote(pubmed_query or query)}&retmax={top_k}"
    )

    try:
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        root = ET.fromstring(res.text)
    except Exception as exc:
        print(f"[Retrieval] PubMed search failed: {exc}")
        return []

    ids = [i.text for i in root.findall(".//Id")]
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

    try:
        res = requests.get(url, timeout=30)
        root = ET.fromstring(res.text)
    except Exception as exc:
        print(f"[Retrieval] PubMed fetch failed: {exc}")
        return []

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
        abstract = " ".join([a.text for a in abstract_parts if a.text])

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
    return {}


def _tokenize(text: str):
    return re.findall(r"[a-z0-9]+", (text or "").lower())


# =========================
# TOOL 4: BM25 SEARCH
# =========================
def bm25_search(query: str, docs: list, top_k: int = 3):
    if not docs:
        return []
    return []


# =========================
# TOOL 5: HYBRID SEARCH
# =========================
def hybrid_search(query: str, docs: list, top_k: int = 3):
    if not docs:
        return []
    return docs[:top_k]


# =========================
# TOOL 6: STORE DOCUMENTS
# =========================
def store_docs(docs):
    return True
