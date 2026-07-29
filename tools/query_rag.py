import chromadb
from sentence_transformers import SentenceTransformer
from langchain_ollama import OllamaLLM

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./medical_db")

collection = client.get_collection("medical_papers")

# Load LLM
llm = OllamaLLM(model="llama3")

while True:
    question = input("\nAsk a question: ")

    if question.lower() == "exit":
        break

    # Convert question to embedding
    query_embedding = model.encode(question).tolist()

    # Search similar chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    context = "\n".join(results["documents"][0])

    prompt = f"""
Use ONLY the context below to answer.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    print("\nAnswer:")
    print(response)