import os
import json
import openai
from llama_index.core import Document
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from fastapi.logger import logger
import logging
from llama_index.core.base.response.schema import Response
from llama_index.core import VectorStoreIndex
import torch
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")
print(openai.api_key)

if not torch.cuda.is_available():
    print("Cuda not available")
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class CustomJSONReader:
    def __init__(self, input_dir):
        self.input_dir = input_dir

    def load_data(self):
        documents = []
        for filename in os.listdir(self.input_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.input_dir, filename), "r") as f:
                    data = json.load(f)
                    for company_data in data: 
                        content = company_data["Description"]
                        content_dict = {"Content": content}
                        documents.append(Document(text=content_dict["Content"]))
        return documents
    

def query_vectorDB(query):
    # Load documents from a directory
    directory = "/home/davidx/Downloads/emerging-tech/server/companyData"
    reader = CustomJSONReader(directory)
    print(reader)
    docs = reader.load_data()
    print(docs)

    # Initalize HuggingFace embedding model
    embedding_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create a vector index
    # index = VectorStoreIndex.from_documents(docs, embed_model=embedding_model)
    index = VectorStoreIndex.from_documents(docs)
    index.storage_context.persist(persist_dir="./vector_db")

    # retriever = VectorIndexRetriever(index=index, similarity_top_k=5)
    # query_engine = index.as_query_engine(response_mode="tree_summarize",retriever = retriever)
    query_engine = index.as_query_engine(response_mode="tree_summarize", similarity_top_k=20)

    response = Response(query_engine.query(query))
    print(response.source_nodes)

    top_companies = []
    for doc in response.source_nodes:
        company_data = json.loads(doc.get_text())
        top_companies.append(company_data)


    return top_companies


print( query_vectorDB("SaaS tool designed for video editors and content creators") )