import streamlit as st
import requests

DEFAULT_API = "http://127.0.0.1:8000/research"


def render_structured_answer(answer):
    if isinstance(answer, dict) and answer.get("papers"):
        st.subheader(answer.get("topic", "Research summary"))
        for i, paper in enumerate(answer["papers"], start=1):
            with st.expander(f"Paper {i}: {paper.get('title', 'Untitled')}", expanded=i == 1):
                st.write(paper.get("summary", ""))
                if paper.get("key_findings"):
                    st.markdown("**Key findings**")
                    for finding in paper["key_findings"]:
                        st.write(f"- {finding}")
                st.markdown(f"**Relevance:** {paper.get('relevance', '')}")
                pmid = paper.get("pmid", "")
                pubmed_url = paper.get("pubmed_url", "")
                if pmid:
                    st.markdown(f"**PMID:** {pmid}")
                if pubmed_url:
                    st.markdown(f"**PubMed URL:** [{pubmed_url}]({pubmed_url})")
    else:
        st.write(answer)

st.set_page_config(page_title="Medical Research Agent", layout="wide")

st.markdown(
    """
    <style>
    .stApp {background: linear-gradient(135deg, #f8fbff 0%, #eef3ff 100%);}
    .block-container {padding-top: 2rem;}
    div[data-testid="stChatMessage"] {border-radius: 16px; padding: 0.4rem 0.2rem;}
    .chat-title {font-size: 2rem; font-weight: 700; margin-bottom: 0.25rem;}
    .chat-subtitle {color: #64748b; margin-bottom: 1rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("⚙️ Settings")
    api_url = st.text_input("API URL", value=DEFAULT_API, key="api_url")
    st.caption("The backend should be running at http://127.0.0.1:8000")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<div class="chat-title">🧠 AtlasAI Medical Research Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-subtitle">Ask about a disease, treatment, or study and get evidence-based answers with PubMed citations.</div>', unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message.get("citations"):
            with st.expander("Sources"):
                for citation in message["citations"]:
                    pmid = citation.get("pmid") or citation.get("id") or ""
                    if pmid:
                        st.write(f"- PMID: {pmid}")

if prompt := st.chat_input("Ask a medical question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching the literature..."):
            try:
                response = requests.post(api_url, json={"question": prompt}, timeout=120)
                response.raise_for_status()
                data = response.json()
            except Exception as exc:
                st.error(f"Request failed: {exc}")
                data = {"answer": "Sorry, I could not reach the backend.", "citations": []}

        answer = data.get("answer", "") or "No answer found."
        citations = data.get("citations", []) or []
        render_structured_answer(answer)
        if citations:
            with st.expander("Sources"):
                for citation in citations:
                    pmid = citation.get("pmid") or citation.get("id") or ""
                    if pmid:
                        st.write(f"- PMID: {pmid}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "citations": citations,
    })