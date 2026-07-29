const axios = require("axios");

// Simple PubMed fetch tool
async function searchPubMed(query) {
  try {
    console.log("🔎 Searching PubMed...");

    const url = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`;

    const searchRes = await axios.get(url, {
      params: {
        db: "pubmed",
        term: query,
        retmode: "json",
        retmax: 3
      }
    });

    const ids = searchRes.data?.esearchresult?.idlist || [];

    if (ids.length === 0) {
      return [];
    }

    // Fetch summaries
    const summaryUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi`;

    const summaryRes = await axios.get(summaryUrl, {
      params: {
        db: "pubmed",
        id: ids.join(","),
        retmode: "json"
      }
    });

    const result = ids.map(id => {
      const item = summaryRes.data.result[id];

      return {
        title: item.title,
        source: "PubMed",
        year: item.pubdate,
        authors: item.authors?.map(a => a.name)
      };
    });

    return result;

  } catch (err) {
    console.error("PubMed error:", err.message);
    return [];
  }
}

module.exports = { searchPubMed };