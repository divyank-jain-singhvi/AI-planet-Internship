import os
import pickle
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader, UnstructuredFileLoader
import langchain
import fitz  # PyMuPDF

def initialize_retrieval(pdf_file_path, model_name='sentence-transformers/all-MiniLM-L6-v2'):
    # Initialize Hugging Face model for embeddings
    model = SentenceTransformer(model_name)

    # Load documents from PDF
    loaders = UnstructuredFileLoader(file_path=pdf_file_path)
    data = loaders.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = text_splitter.split_documents(data)

    # Create embeddings of the chunks
    texts = [doc.page_content for doc in docs]
    embeddings = model.encode(texts, show_progress_bar=True)

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    # Save the FAISS index
    faiss.write_index(index, "index.faiss")

    # Save the documents
    with open("documents.pkl", "wb") as f:
        pickle.dump(docs, f)

    return index, docs, model

def load_index_and_documents():
    # Load the FAISS index
    index = faiss.read_index("index.faiss")

    # Load the documents
    with open("documents.pkl", "rb") as f:
        docs = pickle.load(f)

    return index, docs

class SimpleRetriever:
    def __init__(self, index, docs, model):
        self.index = index
        self.docs = docs
        self.model = model

    def retrieve(self, query, top_k=5):
        query_embedding = self.model.encode(query)
        D, I = self.index.search(np.array([query_embedding]), top_k)
        return [self.docs[i] for i in I[0]]

def retrieval_qa_with_sources(query, retriever, top_k=5):
    documents = retriever.retrieve(query, top_k=top_k)
    unique_documents = []
    unique_sources = set()
    for doc in documents:
        if doc.metadata['source'] not in unique_sources:
            unique_documents.append(doc)
            unique_sources.add(doc.metadata['source'])
    sources = "\n".join([f"{i+1}. {doc.metadata['source']}" for i, doc in enumerate(unique_documents)])
    answer = "\n".join([doc.page_content for doc in unique_documents])
    return {"answer": answer, "sources": sources}
df_file_path =''
# Example usage:
def model(file):
    global pdf_file_path 
    # Initialize retrieval system
    pdf_file_path = 'D:/Full stack pdf analyze project/backend/uploaded file/'+file
def response(question):
    index, docs, model = initialize_retrieval(pdf_file_path)

    # Load index and documents
    index, docs = load_index_and_documents()

    # Create retriever
    retriever = SimpleRetriever(index, docs, model)

    # Define query
    query = question

    # Perform retrieval
    response = retrieval_qa_with_sources(query, retriever)
    return response
