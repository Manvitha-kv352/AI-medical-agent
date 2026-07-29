import requests
import xml.etree.ElementTree as ET
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_ollama import OllamaLLM

# -----------------------------
# INIT MODELS (LOAD ONCE)
# -----------------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

llm = OllamaLLM(model="llama3")

# -----------------------------
# USER QUERY
# -----------------------------
query = input("Enter medical question: ")

# -----------------------------
# STEP 1: PUBMED SEARCH
# -----------------------------
search_url = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    f"esearch.fcgi?db=pubmed&term={query}&retmax=5"
)

search_response = requests.get(search_url)
root = ET.fromstring(search_response.text)

ids = [id_elem.text for id_elem in root.findall(".//Id")]

print(f"\nFound {len(ids)} papers")

# -----------------------------
# STEP 2: FETCH PAPERS
# -----------------------------
id_string = ",".join(ids)

fetch_url = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    f"efetch.fcgi?db=pubmed&id={id_string}&retmode=xml"
)

fetch_response = requests.get(fetch_url)
fetch_root = ET.fromstring(fetch_response.text)

documents = []

for article in fetch_root.findall(".//PubmedArticle"):

    pmid = article.findtext(".//PMID")
    title = article.findtext(".//ArticleTitle")

    abstract_parts = article.findall(".//AbstractText")

    abstract_texts = []
    for part in abstract_parts:
        if part.text:
            abstract_texts.append(part.text)

    abstract = " ".join(abstract_texts)

    if abstract:
        documents.append({
            "text": f"TITLE: {title}\nABSTRACT: {abstract}",
            "pmid": pmid
        })

print(f"Loaded {len(documents)} abstracts")

# -----------------------------
# STEP 3: EMBEDDINGS
# -----------------------------
texts = [d["text"] for d in documents]
embeddings = embedding_model.encode(texts).tolist()

# -----------------------------
# STEP 4: CHROMADB (PERSISTENT)
# -----------------------------
client = chromadb.PersistentClient(path="./medical_db")

collection = client.get_or_create_collection(
    name="pubmed_research"
)

# clear old data
try:
    old = collection.get()
    if old["ids"]:
        collection.delete(ids=old["ids"])
except:
    pass

# store data
for i, doc in enumerate(documents):
    collection.add(
        ids=[str(i)],
        documents=[doc["text"]],
        embeddings=[embeddings[i]],
        metadatas=[{"pmid": doc["pmid"]}]
    )

# -----------------------------
# STEP 5: RETRIEVAL
# -----------------------------
query_embedding = embedding_model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

context_docs = results["documents"][0]
context_meta = results["metadatas"][0]

context = ""
citations = []

for doc, meta in zip(context_docs, context_meta):
    pmid = meta.get("pmid", "Unknown")
    context += doc + "\n\n"
    citations.append(pmid)

# -----------------------------
# STEP 6: LLM PROMPT
# -----------------------------
prompt = f"""
You are a medical research assistant.

RULES:
- Use ONLY the provided context
- Do NOT use outside knowledge
- Every answer should be evidence-based
- Mention PMIDs when relevant
- If not found, say "Not found in provided studies"

Context:
{context}

Question:
{query}
"""

response = llm.invoke(prompt)

# -----------------------------
# STEP 7: OUTPUT
# -----------------------------
print("\n" + "=" * 80)
print("ANSWER:\n")
print(response)

print("\nCITED PMIDs:")
print(", ".join(citations))