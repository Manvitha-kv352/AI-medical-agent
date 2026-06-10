const { addDocuments } = require("./chroma");

async function runIngestion() {
  const docs = [
    "Diabetes is a chronic metabolic disorder affecting insulin regulation.",
    "Hypertension increases risk of heart attack and stroke.",
    "Cancer involves uncontrolled cell growth and division.",
    "Asthma is a respiratory condition causing breathing difficulty.",
    "COVID-19 affects respiratory system and immune response."
  ];

  const result = await addDocuments(docs);

  console.log("✅ RAG Ingestion Done:", result);
}

runIngestion();