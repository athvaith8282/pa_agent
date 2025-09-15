from langchain_openai import ChatOpenAI

# from langchaingoogle_genai import ChatGoogleGenerativeAI


# llm = ChatGoogleGenerativeAI( 
#     model="gemini-2.5-flash",
#     disable_streaming = False
# )

llm_openai = ChatOpenAI(name="gpt-5",streaming=True)