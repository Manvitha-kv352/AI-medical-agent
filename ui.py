import streamlit as st
import requests
from datetime import datetime

DEFAULT_API = "http://127.0.0.1:8000/research"

st.set_page_config(page_title="Medical Research AI", layout="wide")

# Sidebar configuration
st.sidebar.header("Settings")
api_url = st.sidebar.text_input("API URL", value=DEFAULT_API, key="api_url")
top_k = st.sidebar.slider("Number of citations to show", min_value=1, max_value=10, value=3, key="top_k")
st.sidebar.markdown("---")
if "history" not in st.session_state:
    st.session_state.history = []


def add_history(q, result):
    st.session_state.history.insert(0, {"q": q, "time": datetime.now().isoformat(), "result": result})
    # keep last 10
    st.session_state.history = st.session_state.history[:10]
st.markdown(
    """
    <style>
    .center {text-align: center}
    .big-title {font-size:32px; font-weight:700}
    .muted {color: #6c757d}
    .card {background: #ffffff; padding:18px; border-radius:8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);}
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="center big-title">🧠 Medical Research Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="center muted">Evidence-based summaries from PubMed. Clear, concise, and citable.</div>', unsafe_allow_html=True)
    st.write("\n")

    with st.form(key="search_form"):
        query = st.text_input("Ask a question about a disease, treatment, or study", key="query_input")
        cols = st.columns([1, 1])
        with cols[0]:
            submit = st.form_submit_button("🔎 Search")
        with cols[1]:
            show_raw = st.checkbox("Show raw JSON")

    st.write("\n")

    if submit:
        if not query or query.strip() == "":
            st.warning("Please enter a query")
        else:
            # Use sidebar values `api_url` and `top_k` defined above
            try:
                with st.spinner("Generating answer..."):
                    resp = requests.get(api_url, params={"q": query}, timeout=60)
                    resp.raise_for_status()
                    data = resp.json()
            except Exception as e:
                st.error(f"Request failed: {e}")
                data = {"answer": "", "citations": []}

            answer = data.get("answer", "No answer found")
            citations = data.get("citations", []) or data.get("docs", []) or []

            # Display answer in a card
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Answer")
            st.markdown(answer)
            st.markdown('</div>')

            st.write("\n")
            with st.expander("Citations", expanded=True):
                if citations:
                    for i, c in enumerate(citations[:top_k], start=1):
                        if isinstance(c, dict):
                            title = c.get("title", f"Paper {i}")
                            pmid = c.get("pmid", "")
                            url = c.get("url", "")
                            st.markdown(f"**{i}. {title}**  \n                                         PMID: {pmid}  ")
                            if url:
                                st.markdown(f"[Open paper]({url})")
                        else:
                            st.markdown(f"{i}. {c}")
                else:
                    st.info("No citations found for this query.")

            if show_raw:
                st.subheader("Raw response")
                st.json(data)

            add_history(query, {"answer": answer, "citations": citations})

with col2:
    st.markdown("### Recent Queries")
    if st.session_state.history:
        for h in st.session_state.history:
            t = h["time"].split("T")[0]
            st.markdown(f"- {t}: {h['q']}")
    else:
        st.info("No recent searches yet.")

    st.markdown("---")
    st.markdown("**Quick tips**")
    st.markdown("- Be specific: include disease, treatment, or population.  \n- Use the sidebar to change backend URL.")