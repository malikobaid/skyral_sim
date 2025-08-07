import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

st.set_page_config(page_title="🚉 Skyral Transport Demo + AI Bot", page_icon="🤖")

# --- Intro and summary ---
st.markdown("""
# 🚉 Skyral Transport Simulation Demo + Project AI Bot

This demo was built for the Skyral Applied Scientist interview process. It showcases how I approach rapid prototyping for agent-based transport modeling, AWS deployment, and code explainability.


""", unsafe_allow_html=True)

st.markdown("---")

# --- Chatbot interface ---

st.markdown("<h1 style='text-align:center;'>🤖 Talk to This Project's AI Bot</h1>", unsafe_allow_html=True)
st.info("""
Ask anything about this demo's code, AWS setup, architecture, project files, or author profile. All answers come **only** from the local project docs and a local LLM..

You can ask:
- “What is the main code structure?”
- “How does the simulation work?”
- “What AWS services are used and why?”
- “Where can I find the source code for the agent model?”
""")


Settings.embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2", device="cpu")


@st.cache_resource
def load_index():
    docs = SimpleDirectoryReader("project_docs").load_data()
    return VectorStoreIndex.from_documents(docs)

def generate_response(query, index):
    llm = Ollama(model="llama3")
    system_prompt = (
        "You are a technical assistant for this project. Use ONLY the provided context below to answer. "
        "Always answer with file names, paths, and code snippets if relevant. "
        "If the user asks for 'how does X work', describe the sequence of logic or reference relevant files. "
        "If the user asks 'where is Y', give the exact path and summary."
        "If unsure, say: 'Sorry, I don't have enough context to answer that. Please contact the author Obaid Malik'"
    )
    retriever = index.as_retriever(similarity_top_k=3)
    context_nodes = retriever.retrieve(query)
    context_texts = [n.text for n in context_nodes]
    if not context_texts or len(" ".join(context_texts)) < 20:
        return "Sorry, I only answer questions about this project."
    full_context = "\n\n".join(context_texts)
    prompt = (
        f"{system_prompt}\n\n"
        f"Context:\n{full_context}\n\n"
        f"User question: {query}\n"
        f"Answer using ONLY the context above."
    )
    resp = llm.complete(prompt)
    return resp.text

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

index = load_index()

# Display chat history (no duplicates)
for is_user, msg in st.session_state.chat_history:
    if is_user:
        st.markdown(f"<div style='text-align:right;color:#15616d;font-size:1.08rem;font-weight:600;'>🧑 {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:left;color:#324fa8;font-size:1.08rem;font-weight:500;'>🤖 {msg}</div>", unsafe_allow_html=True)

# Use a form to manage input/submit
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask about this project...", key="chat_input", label_visibility="visible", placeholder="Type your question and press Enter...")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    # Prevent duplicates
    if not st.session_state.chat_history or st.session_state.chat_history[-1][1] != user_input:
        st.session_state.chat_history.append((True, user_input))
        with st.spinner("Thinking..."):
            reply = generate_response(user_input, index)
        st.session_state.chat_history.append((False, reply))
        st.rerun()  # Only rerun after new submission
