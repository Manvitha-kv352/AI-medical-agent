from fastapi import FastAPI
import chromadb
from sentence_transformers import SentenceTransformer

app = FastAPI()

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("medical")

@app.post("/ingest")
def ingest(data: dict):
    docs = data["docs"]

    embeddings = model.encode(docs).tolist()
    ids = [str(i) for i in range(len(docs))]

    collection.add(
        documents=docs,
        embeddings=embeddings,
        ids=ids
    )

    return {"status": "ingested", "count": len(docs)}

@app.post("/search")
def search(data: dict):
    query = data["query"]

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    return {
        "documents": results["documents"][0]
    }