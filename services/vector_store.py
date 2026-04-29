from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_vectorstore(mode):
    if mode == "Single PDF":
        loader = PyPDFLoader("data/sample.pdf")
    else:
        loader = DirectoryLoader("data/", glob="**/*.pdf", loader_cls=PyPDFLoader)

    docs = loader.load()

    if not docs:
        return None

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.split_documents(docs)

    embeddings = FakeEmbeddings(size=384)

    return FAISS.from_documents(docs, embeddings)