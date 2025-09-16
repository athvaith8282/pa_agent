from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv
import time
import config as cfg

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker

pdfs = [
    '/Users/athvaithk/Desktop/LLM/projects/PA_AGENT/retriever/data/boost_energy.pdf',
    '/Users/athvaithk/Desktop/LLM/projects/PA_AGENT/retriever/data/carvings.pdf',
    '/Users/athvaithk/Desktop/LLM/projects/PA_AGENT/retriever/data/loctose_intolerance.pdf'   
]

# Init once
embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
text_splitter = SemanticChunker(embedding_model)

chromadb = Chroma(
    collection_name="banner_health_blogs",
    embedding_function=embedding_model,  # required, but we’ll feed precomputed embeddings
    persist_directory=cfg.VEC_DB_PATH,
)

# Page-wise ingestion
for pdf_path in pdfs:
    pdf_loader = PyPDFLoader(pdf_path)
    pages = [page.page_content for page in pdf_loader.lazy_load()]
    docs = text_splitter.create_documents(pages)
    time.sleep(60)
    chromadb.add_documents( 
        docs
    )