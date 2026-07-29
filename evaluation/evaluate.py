import json
import sys
from pathlib import Path
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api import app as fastapi_app

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "sample_dataset.json"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_PATH = RESULTS_DIR / "predictions.json"

client = TestClient(fastapi_app)

with DATASET_PATH.open("r", encoding="utf-8") as f:
    dataset = json.load(f)

results = []

for item in dataset:
    question = item["question"]

    response = client.get("/research", params={"q": question})
    response.raise_for_status()

    data = response.json()

    results.append({
        "question": question,
        "answer": data["answer"],
        "context": data["context"],
        "pmids": data["pmids"]
    })

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

with RESULTS_PATH.open("w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)

print(f"Evaluation results written to {RESULTS_PATH}")