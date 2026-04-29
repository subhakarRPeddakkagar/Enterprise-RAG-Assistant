from services.llm_service import get_llm
from services.vector_store import load_vectorstore

def get_chain(mode):
    llm = get_llm()

    # 🟢 LLM ONLY
    if mode == "LLM Only":
        def run(query):
            return {"answer": llm.invoke(query).content}
        return run

    # 🟡🔵 RAG MODES
    vectorstore = load_vectorstore(mode)

    if vectorstore is None:
        return None

    retriever = vectorstore.as_retriever()

    def run(query):
        docs = retriever.invoke(query)
        context = " ".join([d.page_content for d in docs])

        response = llm.invoke(f"Context: {context}\nQuestion: {query}")

        return {
            "answer": response.content,
            "sources": docs
        }

    return run