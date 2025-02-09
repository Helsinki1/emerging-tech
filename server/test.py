import os
import json
import faiss
from llama_index.core import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import (
    SimpleDirectoryReader,
    load_index_from_storage,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor


# Load JSON files from the directory
def load_json_files(directory):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), "r") as file:
                data = json.load(file)
                all_data.extend(data)  # Assuming the data is a list of dicts
    return all_data

# Example function to build the vector store
def build_rag_index(data):
    # Extract relevant fields
    documents = []
    for entry in data:
        doc = Document(
            text=entry["Description"],  # Use the company description as the document text
            doc_id=entry["Name"]        # Use the company name as the document ID
        )
        documents.append(doc)

    d = 1536
    faiss_index = faiss.IndexFlatL2(d)

    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )

    return index

# Function to query the RAG index
def query_rag_index(query, index):
    retriever = index.as_query_engine(similarity_top_k=5)
    response = retriever.query(query)
    return response

# Main function to load the data, build the RAG, and query
def main():
    directory = "/home/davidx/Downloads/emerging-tech/server/companyData"  # Path to your JSON files directory
    data = load_json_files(directory)
    rag_index = build_rag_index(data)
    
    # Example query (description of a company)
    query = "innovative security solution designed specifically to protect API"
    
    # Query the RAG index
    response = query_rag_index(query, rag_index)
    print(f"Response: {response}")




#if __name__ == "__main__":
    #main()

