import streamlit as st
import os
import sys

sys.path.append(os.path.abspath("."))

from chains.chat_chain import get_chain

st.set_page_config(page_title="Enterprise Knowledge Assistant", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Settings")

# ✅ ADD MODE SELECTOR (MISSING)
mode = st.sidebar.selectbox(
    "Choose Mode",
    ["LLM Only", "Single PDF", "Multiple PDFs"]
)

uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    if not os.path.exists("data"):
        os.makedirs("data")

    for file in uploaded_files:
        with open(f"data/{file.name}", "wb") as f:
            f.write(file.getbuffer())

    st.sidebar.success("Files uploaded!")

# ---------------- MAIN ----------------
st.title("💬 Enterprise Knowledge Assistant")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # ✅ FIX: pass mode
    chain = get_chain(mode)

    if chain is None:
        st.warning("⚠️ Please upload PDF(s) first!")
        st.stop()

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            # ✅ FIX: new function call (not dict)
            response = chain(user_input)

            answer = response["answer"]

            st.markdown(answer)

            # ✅ Show sources only in RAG
            if mode != "LLM Only" and "sources" in response:
                st.markdown("### 📄 Sources:")
                for i, doc in enumerate(response["sources"][:3]):
                    st.markdown(f"Source {i+1}")

    st.session_state.messages.append({"role": "assistant", "content": answer})