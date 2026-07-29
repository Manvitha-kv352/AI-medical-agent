from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

# Load PDF
pdf_path = r"C:\Users\MANVITH\OneDrive\Desktop\type 2 diabetes review.pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text

# Create chunks
chunk_size = 1000

chunks = []

for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i + chunk_size])

print(f"Created {len(chunks)} chunks")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
embeddings = model.encode(chunks).tolist()

# Create ChromaDB
client = chromadb.PersistentClient(path="./medical_db")

collection = client.get_or_create_collection(
    name="medical_papers"
)

# Store chunks
for i, chunk in enumerate(chunks):
    collection.add(
        ids=[str(i)],
        documents=[chunk],
        embeddings=[embeddings[i]]
    )

print("Vector database created successfully!")