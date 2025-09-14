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