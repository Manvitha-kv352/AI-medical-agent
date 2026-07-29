import requests
import xml.etree.ElementTree as ET

query = input("Enter medical query: ")

# Search PubMed
search_url = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    f"esearch.fcgi?db=pubmed&term={query}&retmax=5"
)

search_response = requests.get(search_url)

root = ET.fromstring(search_response.text)

ids = [id_elem.text for id_elem in root.findall(".//Id")]

print(f"\nFound {len(ids)} papers\n")

# Fetch details
id_string = ",".join(ids)

fetch_url = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    f"efetch.fcgi?db=pubmed&id={id_string}&retmode=xml"
)

fetch_response = requests.get(fetch_url)

fetch_root = ET.fromstring(fetch_response.text)

for article in fetch_root.findall(".//PubmedArticle"):

    title = article.findtext(".//ArticleTitle")

    abstract_parts = article.findall(".//AbstractText")

    abstract_texts = []

    for part in abstract_parts:
        if part.text:
            abstract_texts.append(part.text)

    abstract = " ".join(abstract_texts)

    if not abstract:
        abstract = "No abstract available."

    print("\n" + "=" * 80)
    print("TITLE:")
    print(title)

    print("\nABSTRACT:")
    print(abstract[:1500])