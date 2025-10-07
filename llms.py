from langchain_openai import ChatOpenAI

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# load_dotenv()

def get_llm_gemini():
    llm_gemini = ChatGoogleGenerativeAI( 
        model="gemini-2.5-flash"
    )
    return llm_gemini

# llm_openai = ChatOpenAI(name="gpt-5",streaming=True)