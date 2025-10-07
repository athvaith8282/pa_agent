import streamlit as st 
import asyncio
import nest_asyncio
nest_asyncio.apply()
# from dotenv import load_dotenv
# load_dotenv()

if "loop" not in st.session_state:
    st.session_state.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(st.session_state.loop)
import os
import json
import uuid
from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage,SystemMessage
from streamlit_oauth import OAuth2Component

import config as cfg
import my_prompts as prm
import utils as utl
from st_callable_util import get_langfuse_callback

from logger_config import get_logger
logger = get_logger()



st.title("PERSONAL ASSISTENT")

st.set_page_config(
    page_title= "PA AGENT",
    initial_sidebar_state="expanded"
)
event_runner = st.session_state.loop.run_until_complete

if "GOOGLE_API_KEY" in st.session_state: 
    os.environ["GOOGLE_API_KEY"] = st.session_state.GOOGLE_API_KEY
    from pa_agent import MyGraph
    from retriever.main import update_retriever


    if "graph" not in st.session_state:
        st.session_state.graph = MyGraph()
        event_runner(st.session_state.graph.build_graph())

    # if "oauth" not in st.session_state:
    #     st.session_state.oauth2 = OAuth2Component(
    #                 client_id=os.getenv("CLIENT_ID"),
    #                 client_secret=os.getenv("CLIENT_SECRET"),
    #                 authorize_endpoint=cfg.GOOGLE_AUTHORIZE_URL,
    #                 token_endpoint=cfg.GOOGLE_TOKEN_URL,
    #                 refresh_token_endpoint=cfg.GOOGLE_REFRESH_TOKEN_URL
    #             )

    with st.sidebar:
        if st.button(
                "New Chat",
                use_container_width=True
            ):
            thread_id = str(uuid.uuid4())
            st.session_state.config = {"configurable": {"thread_id": thread_id}}
            current_date = datetime.now().strftime("%B %d, %Y")
            st.session_state.messages =  [
                SystemMessage(content=prm.SYSTEM_PROMPT.format(date=current_date)),
                AIMessage(content="Hello, How Can I help You !!")
            ]
        
        # st.title("Permission:")
        # with st.expander("OAuth", expanded=True):
        #     if "gmail_token" not in st.session_state:
        #         if os.path.exists(cfg.TOKEN_PATH):
        #             with open(cfg.TOKEN_PATH, 'r') as file:
        #                 token = json.load(file)
        #                 try:
        #                     gmail_token = st.session_state.oauth2.refresh_token( 
        #                         token=token,
        #                         force=False
        #                     )
        #                     st.session_state.gmail_token = gmail_token
        #                     event_runner(st.session_state.graph.rebuild_graph(st.session_state.gmail_token))
        #                     st.success("✅ Gmail authorization successful!")
        #                     st.rerun()
        #                 except Exception as e:
        #                     logger.exception(e)
        #                     event_runner(utl.get_gmail_token())
                            
        #         else:
        #             event_runner(utl.get_gmail_token())
        #     else:
        #         # Token exists, show controls
        #         with open(cfg.TOKEN_PATH, 'w') as file:
        #             json.dump(st.session_state.gmail_token, file)
        #         st.success("✅ Gmail authorized!")
        
        st.title("Uploader:")
        with st.expander("Upload a PDF", expanded=True):
            upload_file = st.file_uploader("Upload a pdf", type="pdf")
            description = st.text_input("Description")
            if st.button("Upload"):
                if not upload_file:
                    st.sidebar.error("Please upload a PDF file.")
                elif not description:
                    st.sidebar.error("Description is required.")
                else:
                    with st.spinner("⏳ Uploading file..."):
                        try:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"{cfg.RETRIEVER_DATA_DIR}/file_{timestamp}.pdf"
                            with open(filename, 'wb') as f:
                                f.write(upload_file.read())
                            update_retriever(filename, description=description)
                            st.sidebar.success("✅ File uploaded successfully!")
                        except Exception as e:
                            logger.exception(e)
                            st.sidebar.error(f"❌ Upload failed: LLM BUSY")                       
        st.title("Chats:")
        with st.expander("Previous Conversations", expanded=True):
            chats = event_runner(st.session_state.graph.get_history())
            if chats:
                for chat in chats:
                    thread_id = chat["thread_id"]
                    first_msg = chat["message"].content
                    display_text = (first_msg[:25] + "...") if len(first_msg) > 25 else first_msg
                    if st.button(display_text, key=thread_id, use_container_width=True):
                        st.session_state.config = {"configurable": {"thread_id": thread_id}}
                        current_state = event_runner(st.session_state.graph.get_chat_block(st.session_state.config))
                        if current_state and current_state.values.get("messages"):
                            st.session_state.messages = current_state.values["messages"]
                        else:
                            st.session_state.messages = [
                                AIMessage(content="Sorry, Can't recieve past conversation")
                            ]
                        st.rerun()

    if "config" not in st.session_state:
        thread_id = str(uuid.uuid4())
        st.session_state.config = {"configurable": {"thread_id": thread_id}}

    if "messages" not in st.session_state:
        current_state = event_runner(st.session_state.graph.get_chat_block(st.session_state.config))
        if current_state and current_state.values.get("messages"):
            st.session_state.messages = current_state.values["messages"]
        else: 
            current_date = datetime.now().strftime("%B %d, %Y")
            st.session_state.messages =  [
                SystemMessage(content=prm.SYSTEM_PROMPT.format(date=current_date)),
                AIMessage(content="Hello, How Can I help You !!")
            ]

    for msg in st.session_state.messages:
        if isinstance(msg, AIMessage):
            if msg.content:
                st.chat_message('assistant').write(msg.content)
        if isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)
    
    # pill_selection = st.pills(
    #     "💡 Quick start ideas:",
    #     cfg.suggestions,
    #     selection_mode="single",
    #     key="quickstart_pills",
    # )
    # if pill_selection:
    #     prompt = pill_selection
    
    if prompt := st.chat_input():
        st.session_state.messages.append(HumanMessage(content=prompt))
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            # st_callback = get_streamlit_cb(st.container())
            langfuse_callback = get_langfuse_callback()
            response = event_runner(
                st.session_state.graph.invoke_graph
                    (st.session_state.messages, 
                    st.session_state.config, 
                    [langfuse_callback]
                    )
            )
            st.session_state.messages.append(AIMessage(content=response))
    
else:
    st.markdown("""
        ⚠️ To run this application, you need a **Google Gemini API key**.  
        You can get a free one at [**Google AI Studio →**](https://aistudio.google.com/)
                
        🔒 Your key is only used locally — it won’t be stored
        """
    )
    gemini_api_key = st.text_input("Gemini API Key", type="password", key="gemini_api_key")

    if st.button("Save API Key"):
        if not gemini_api_key:
            st.error("Please enter your Gemini API key.")
        else:
            st.session_state.GOOGLE_API_KEY = gemini_api_key
            st.success("✅ Gemini API key saved successfully!")
            st.rerun()