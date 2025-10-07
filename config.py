import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_DIR = os.path.join(DATA_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "pa_agent.sqlite")

TOKEN_DIR = os.path.join(DATA_DIR, "google_tokens")
TOKEN_PATH = os.path.join(TOKEN_DIR, "token.json")
SCOPES= "https://www.googleapis.com/auth/gmail.modify"

CLIENT_DIR= os.path.join(DATA_DIR, "google_client")
CLIENT_PATH= os.path.join(CLIENT_DIR, "web_client_google.json")

GOOGLE_AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_REFRESH_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_REVOKE_TOKEN_URL = "https://oauth2.googleapis.com/revoke"

REDIRECT_URI = "http://localhost:8501/component/streamlit_oauth.authorize_button"

VEC_DB_DIR = os.path.join(DATA_DIR, 'vectordb')
VEC_DB_PATH = os.path.join(VEC_DB_DIR, 'blogs_chroma_db')
VEC_COLLECTION_NAME = "banner_health_blogs"
VEC_EMBEDDING_NAME = "models/gemini-embedding-001"

LOGS_DIR = os.path.join(BASE_DIR, 'logs')
LOGS_PATH = os.path.join(LOGS_DIR, 'pa_agent.log')

MCP_CONFIG = {
        "F1_MCP": {
            "command": "python3",
            "args": ["my_mcp/main.py"],
            "transport": "stdio",
        }
}

RETRIEVER_DATA_DIR = os.path.join(BASE_DIR, 'retriever/data')
RETRIEVER_STATUS_FILE = os.path.join(RETRIEVER_DATA_DIR, "status_retriever.json")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(TOKEN_DIR, exist_ok=True)
os.makedirs(CLIENT_DIR, exist_ok=True)
os.makedirs(VEC_DB_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(RETRIEVER_DATA_DIR, exist_ok=True)