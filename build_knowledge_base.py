import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

# 1. load the document(s)
KNOWLEDGE_BASE_SRC_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base_srcs")
documents = []
for file in os.listdir(KNOWLEDGE_BASE_SRC_PATH):
    loader = PyPDFLoader(os.path.join(KNOWLEDGE_BASE_SRC_PATH, file))
    document = loader.load()
    documents.extend(document)
# 2. split the document into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)

# 3. create embeddings and build the FAISS vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = FAISS.from_documents(chunks, embeddings)

# 4. save the vector store to disk
vector_store.save_local("faiss_index")
print(f"Knowledge base created from {len(documents)} pages, {len(chunks)} chunks.")