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

SystemPrompt = """
You are a personal assistant. You will answer the user's questions using the given tools if needed.

- You have access to Gmail tools. Help the user read, draft, and send mails if asked.
- You have access to F1-tools. Use them to fetch F1 calendar, driver, and constructor results for a particular year.
_ You have access to some health blogs. Use this tool to answers questions regarding particular topics mentioned by tool.
- Always choose the appropriate tool when required.
"""

VEC_DB_DIR = os.path.join(DATA_DIR, 'vectordb')
VEC_DB_PATH = os.path.join(VEC_DB_DIR, 'blogs_chroma_db')