import requests
import xml.etree.ElementTree as ET

query = input("Enter medical query: ")

url = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    f"esearch.fcgi?db=pubmed&term={query}&retmax=5"
)

response = requests.get(url, timeout=30)

root = ET.fromstring(response.text)

print("\nPubMed IDs:\n")

for id_elem in root.findall(".//Id"):
    print(id_elem.text)