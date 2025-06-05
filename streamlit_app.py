
import os
import datetime
import time
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from api.arxiv_fetcher import search_arxiv
from agents.paper_agent import summarize_papers
from agents.plot_agent import extract_metrics, plot_metrics

# ------------------------
# 🎨 Page Configuration & CSS Styling
# ------------------------
st.set_page_config(page_title="Multi-Agent Scientific Assistant", layout="wide")

st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
        }
        .stButton>button {
            background-color: #4a90e2;
            color: white;
            padding: 10px 16px;
            border-radius: 8px;
            font-weight: 600;
        }
        .stTextInput>div>input {
            background-color: #f0f4f8;
            border-radius: 8px;
        }
        .block-container {
            padding-top: 2rem;
        }
        footer {
            visibility: hidden;
        }
        .custom-footer {
            position: fixed;
            bottom: 10px;
            left: 0;
            right: 0;
            text-align: center;
            color: grey;
            font-size: 14px;
        }
    </style>
    <div class="custom-footer">
        Built by <a href="https://github.com/Jatin1230" target="_blank">Jatin Chopra</a> |
        <a href="https://www.linkedin.com/in/jatin-chopra-503118188/" target="_blank">LinkedIn</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align: center;'>🧠 Multi-Agent Scientific Research Assistant</h1>
<h4 style='text-align: center; color: grey;'>Summarize, Compare, and Visualize Scientific Papers with AI Agents</h4>
""", unsafe_allow_html=True)
st.divider()

# ------------------------
# 📁 Sidebar
# ------------------------
with st.sidebar:
    st.image("logo.png", width=120)
    st.markdown("## ⚙️ Settings")
    model = st.selectbox("LLM Model", ["DeepSeek R1", "GPT-3.5", "Gemini Pro"])
    st.markdown("---")
    st.markdown("### 🧠 Active Agents")
    st.info("📄 PaperAgent\n📊 PlotAgent")

# ------------------------
# 🔍 Input Section
# ------------------------
st.markdown("### 🔬 Enter a research topic or upload PDF papers")

col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("Enter a research topic", placeholder="e.g., Diffusion Models in NLP")
with col2:
    max_results = st.selectbox("📄 Papers to fetch", [3, 5, 7])

uploaded_files = st.file_uploader("📄 Upload your own research papers (PDFs)", type=["pdf"], accept_multiple_files=True)
btn = st.button("🚀 Run Agents")

# ------------------------
# 🧠 PDF Loader
# ------------------------
def load_multiple_pdfs(files):
    papers = []
    for file in files:
        temp_path = f"./temp_{file.name}"
        with open(temp_path, "wb") as f:
            f.write(file.read())

        loader = PyPDFLoader(temp_path)
        pages = loader.load()
        text = "\n".join([p.page_content for p in pages])
        papers.append({
            "title": file.name,
            "summary": text[:3000],
            "link": "Uploaded File"
        })
    return papers

# ------------------------
# 🚀 Agent Flow + Tabbed UI with Loading Animation
# ------------------------
if btn and (query or uploaded_files):
    st.toast("Agents activated!")

    placeholder = st.empty()
    with placeholder.container():
        with st.spinner("🔍 Preparing your research analysis..."):
            time.sleep(1.2)

    if uploaded_files:
        with st.spinner("📄 Loading uploaded PDFs..."):
            papers = load_multiple_pdfs(uploaded_files)
    else:
        with st.spinner("📡 Fetching papers from arXiv..."):
            papers = search_arxiv(query, max_results)

    with st.spinner("🧠 Summarizing with PaperAgent..."):
        summary = summarize_papers(papers)
    metrics = extract_metrics(summary)

    # ----- Tabbed Results Layout -----
    tab1, tab2, tab3 = st.tabs(["📄 Papers", "🧠 Summary", "📊 Visualization"])

    with tab1:
        st.subheader("📄 Uploaded or Fetched Papers")
        for i, p in enumerate(papers, 1):
            with st.expander(f"{i}. {p['title']}"):
                st.markdown(p["summary"])
                st.markdown(f"[🔗 {p['link']}]({p['link']})")

    with tab2:
        st.subheader("🧠 AI Summary")
        st.markdown(summary)
        st.download_button(
            label="⬇️ Download Summary (Markdown)",
            file_name=f"summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            data=f"# Research Summary\n\n{summary}"
        )

    with tab3:
        st.subheader("📊 PlotAgent Visualization")
        if metrics:
            plot_metrics(metrics)
        else:
            st.info("⚠️ PlotAgent couldn't detect any numeric metrics to visualize.")

elif btn and not query and not uploaded_files:
    st.warning("⚠️ Please enter a topic or upload at least one PDF to begin.")
