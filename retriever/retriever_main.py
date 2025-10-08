import json
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker

import config as cfg
from utils import retry
from logger_config import get_logger

logger = get_logger()

# Init once
embedding_model = GoogleGenerativeAIEmbeddings(model=cfg.VEC_EMBEDDING_NAME)
text_splitter = SemanticChunker(embedding_model)

with open(cfg.RETRIEVER_STATUS_FILE, 'r') as f:
      status_retriever = json.load(f)

chromadb = Chroma(
    collection_name=cfg.VEC_COLLECTION_NAME,
    embedding_function=embedding_model,  # required, but we’ll feed precomputed embeddings
    persist_directory=cfg.VEC_DB_PATH,
)

@retry(max_attempts=3, delay=30)
def pages_to_docs(pages):
    return text_splitter.create_documents(pages)

# Page-wise ingestion
@retry(max_attempts=3, delay=30)
def update_retriever(pdf_path, description):
        if pdf_path in status_retriever.keys():
              if status_retriever[pdf_path]["status"] == "Done":
                    return
        status_retriever[pdf_path] = {
              "description" : description,
              "status": "Pending"
        }
        with open(cfg.RETRIEVER_STATUS_FILE, 'w') as f:
            json.dump(status_retriever, f)
        pdf_loader = PyPDFLoader(pdf_path)
        pages = [page.page_content for page in pdf_loader.lazy_load()]
        docs = pages_to_docs(pages=pages)
        chromadb.add_documents( 
            docs
        )
        status_retriever[pdf_path]["status"] = "Done"

        with open(cfg.RETRIEVER_STATUS_FILE, 'w') as f:
            json.dump(status_retriever, f)
        return True