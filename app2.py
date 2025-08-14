import streamlit as st
from utils import read_file
from processors.clause_simplifier import simplify_clause
from processors.ner_extractor import extract_entities
from processors.clause_extractor import extract_clauses
from processors.doc_classifier import classify_document

# ---------------------- Theming & Global UI (UI only) ----------------------
st.set_page_config(page_title="ClauseWise - Legal Document Analyzer", layout="wide", initial_sidebar_state="expanded")

# Custom CSS: law-themed palette (navy/gold), cards, subtle animations
st.markdown("""
<style>
/* Background & typography */
html, body, [data-testid="stAppViewContainer"] > .main {
  background: radial-gradient(1200px 700px at 85% -10%, rgba(199,163,24,0.12), transparent 60%),
              linear-gradient(180deg, #0b1e39 0%, #0a1730 45%, #0a1429 100%);
  color: #f6f7fb;
  font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif;
}

/* Sidebar animation toggle */
.sidebar-toggle {
  position: fixed;
  left: 250px;
  top: 20px;
  background: #c7a318;
  color: #0b1e39;
  padding: 6px 10px;
  border-radius: 999px;
  font-weight: bold;
  cursor: pointer;
  z-index: 9999;
  transition: all 0.3s ease-in-out;
}
.sidebar-collapsed .sidebar-toggle {
  left: 10px;
}
.sidebar-hidden section[data-testid="stSidebar"] {
  transform: translateX(-250px);
}
section[data-testid="stSidebar"] {
  transition: transform 0.3s ease-in-out;
}

/* Streamlit default widgets refinements */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0a1730, #0b1e39);
  border-right: 1px solid rgba(255,255,255,0.06);
}

div[data-baseweb="select"] > div, .stTextArea textarea, .stFileUploader {
  border-radius: 14px !important;
}

.stFileUploader {
  background: rgba(255,255,255,0.03);
  border: 1px dashed rgba(199,163,24,0.45);
  padding: 16px;
}

/* Title bar */
.hero {
  display: flex; align-items: center; gap: 14px;
  margin-bottom: 10px;
}
.hero-badge {
  background: linear-gradient(135deg, #c7a318, #e1c05a);
  color: #0b1e39; font-weight: 700; font-size: 12px; padding: 6px 10px; border-radius: 999px;
  letter-spacing: .08em; text-transform: uppercase;
}
.hero-title {
  font-size: 40px; /* increased from 32px */
  font-weight: 800; letter-spacing: .3px;
}
.hero-sub {
  color: #b9c4d6; margin-top: -4px; font-size: 14px;
}

/* Cards */
.card {
  background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 18px;
  padding: 18px 18px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  backdrop-filter: blur(6px);
}

/* Section headers with animated accent rule */
.section {
  margin-top: 8px;
  padding-top: 6px;
  position: relative;
}
.section h3 {
  display: inline-flex; align-items: center; gap: 8px;
  font-weight: 800; letter-spacing: .2px; margin-bottom: 12px;
}
.section:after {
  content: ""; position: absolute; left: 0; bottom: -8px; height: 2px;
  width: 0; background: linear-gradient(90deg,#e1c05a,#c7a318);
  animation: grow 1.1s ease forwards;
}
@keyframes grow { to { width: 100%; } }

/* “Clause” badges & simplified text contrast */
.badge {
  display: inline-block; padding: 4px 10px; border-radius: 999px;
  background: rgba(199,163,24,0.18); color: #f6f1dd; border: 1px solid rgba(199,163,24,0.35);
  font-size: 12px; font-weight: 700; letter-spacing: .04em;
}
.clause {
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px; padding: 12px; margin-top: 8px;
}
.simplified {
  background: rgba(10,255,120,0.06); border: 1px solid rgba(10,255,120,0.18);
  border-radius: 14px; padding: 12px; margin-top: 8px;
}

/* Animated divider */
.hr {
  height: 1px; border: none; margin: 18px 0;
  background: linear-gradient(90deg, transparent, rgba(225,192,90,.6), transparent);
  position: relative; overflow: hidden;
}
.hr:before {
  content:""; position:absolute; left:-30%; top:0; height:100%; width:30%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,.6), transparent);
  animation: sweep 2.8s ease-in-out infinite;
  filter: blur(2px);
}
@keyframes sweep { 50% { left: 100%; } 100% { left: 100%; } }

/* Subtle hover rise */
.rise { transition: transform .2s ease, box-shadow .2s ease; }
.rise:hover { transform: translateY(-2px); box-shadow: 0 14px 36px rgba(0,0,0,0.28); }

/* Make JSON blocks blend with theme */
[data-testid="stJson"] pre {
  background: rgba(0,0,0,0.25) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 12px !important;
  padding: 12px !important;
  color: #e8eef8 !important;
}

/* Toast tweak */
div[role="alert"] {
  border-radius: 12px !important;
}
</style>
<script>
function toggleSidebar() {
  const app = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
  const sidebar = window.parent.document.querySelector('section[data-testid="stSidebar"]');
  app.classList.toggle('sidebar-hidden');
}
</script>
""", unsafe_allow_html=True)

# Sidebar toggle button
st.markdown('<div class="sidebar-toggle" onclick="toggleSidebar()">⇦</div>', unsafe_allow_html=True)

# ---------------------- Header ----------------------
st.markdown(
    """
    <div class="hero">
      <div class="hero-badge">ClauseWise</div>
      <div>
        <div class="hero-title">📜 Legal Document Analyzer</div>
        <div class="hero-sub">Analyze contracts with entity extraction, clause simplification, and type classification.</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------- Sidebar ----------------------
with st.sidebar:
    st.markdown("### ⚖️ ClauseWise")
    st.caption("Precision insights for legal documents.")
    st.markdown("---")
    st.markdown("**Tips**")
    st.write("- PDF, DOCX, or TXT supported\n- Paste text if you don’t have a file\n- Results appear in elegant sections")
    st.markdown("---")
    colA, colB = st.columns(2)
    with colA:
        st.metric("Accuracy", "High")
    with colB:
        st.metric("Speed", "Fast")
    st.markdown("---")
    st.caption("© ClauseWise • Crafted for legal workflows")

# ---------------------- Main Input Card ----------------------
st.markdown('<div class="card rise">', unsafe_allow_html=True)
st.subheader("📁 Upload or Paste", divider=False)
st.caption("Securely process your document or paste plain text below.")

uploaded_file = st.file_uploader("Upload a legal document", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner("Processing document…"):
        text = read_file(uploaded_file)
else:
    text = st.text_area("Or paste your text here", height=180, placeholder="Paste contract text…")

st.markdown('</div>', unsafe_allow_html=True)

if text.strip():
    st.markdown('<div class="card section rise">', unsafe_allow_html=True)
    st.markdown('<h3>📄 Document Type Classification</h3>', unsafe_allow_html=True)
    with st.spinner("Classifying document…"):
        classification = classify_document(text)
        st.json(classification)
    st.markdown('<hr class="hr" />', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card section rise">', unsafe_allow_html=True)
    st.markdown('<h3>🏷 Named Entities</h3>', unsafe_allow_html=True)
    with st.spinner("Extracting named entities…"):
        entities = extract_entities(text)
        st.json(entities)
    st.markdown('<hr class="hr" />', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card section rise">', unsafe_allow_html=True)
    st.markdown('<h3>✂ Clause Extraction & Simplification</h3>', unsafe_allow_html=True)
    with st.spinner("Extracting and simplifying clauses…"):
        clauses = extract_clauses(text)
        for i, clause in enumerate(clauses, 1):
            st.markdown(f'<span class="badge">Clause {i}</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="clause">{clause}</div>', unsafe_allow_html=True)
            simplified = simplify_clause(clause)
            st.markdown(f'<div class="simplified"><strong>Simplified:</strong> {simplified}</div>', unsafe_allow_html=True)
            st.markdown('<hr class="hr" />', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Please upload a document or paste text to analyze.")
