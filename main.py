import streamlit as st 
import os
import json
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from streamlit_oauth import OAuth2Component

import config as cfg
from pa_agent import MyGraph
from st_callable_util import get_streamlit_cb
import nest_asyncio

nest_asyncio.apply()
import asyncio

if "loop" not in st.session_state:
    st.session_state.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(st.session_state.loop)


if "config" not in st.session_state:
    st.session_state.config = {"configurable": {"thread_id": "chat3"}}

if "graph" not in st.session_state:
    st.session_state.graph = MyGraph()
    st.session_state.loop.run_until_complete(st.session_state.graph.build_graph())

if "messages" not in st.session_state:
    current_state = st.session_state.loop.run_until_complete(st.session_state.graph.get_chat_block(st.session_state.config))
    if current_state and current_state.values.get("messages"):
        st.session_state.messages = current_state.values["messages"]
    else: 
        st.session_state.messages =  [AIMessage(content="Hello, How Can I help You !!")]

st.title("PERSONAL ASSISTENT")

oauth2 = OAuth2Component(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        authorize_endpoint=cfg.GOOGLE_AUTHORIZE_URL,
        token_endpoint=cfg.GOOGLE_TOKEN_URL,
        refresh_token_endpoint=cfg.GOOGLE_REFRESH_TOKEN_URL
    )

if "gmail_token" not in st.session_state:
    
    if os.path.exists(cfg.TOKEN_PATH):
        with open(cfg.TOKEN_PATH, 'r') as file:
            token = json.load(file)
            st.session_state.gmail_token = oauth2.refresh_token( 
                token=token,
                force=False
            )
            st.session_state.graph.rebuild_graph(st.session_state.gmail_token)
            st.success("✅ Gmail authorization successful!")
            st.rerun()
    else:
        st.warning("⚠️ Please authorize Gmail access")
        
        # Show authorize button
        result = oauth2.authorize_button(
            name="🔐 Authorize Gmail",
            redirect_uri=cfg.REDIRECT_URI,
            scope=cfg.SCOPES,
            key="gmail_auth",
            use_container_width=True,
            extras_params={"prompt": "consent", "access_type": "offline"}
        )
        
        if result and 'token' in result:
            with open(cfg.TOKEN_PATH, 'w') as file:
                json.dump(result["token"], file)
            st.session_state.gmail_token = result['token']
            st.session_state.graph.rebuild_graph(st.session_state.gmail_token)
            st.success("✅ Gmail authorization successful!")
            st.rerun()
else:
        # Token exists, show controls
        with open(cfg.TOKEN_PATH, 'w') as file:
            json.dump(st.session_state.gmail_token, file)
        st.success("✅ Gmail authorized!")

for msg in st.session_state.messages:
    if isinstance(msg, AIMessage):
        if msg.content:
            st.chat_message('assistant').write(msg.content)
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    if isinstance(msg, ToolMessage):
        with st.chat_message("tool"):
            tool_placeholder = st.empty()
            with tool_placeholder.status(f"Tool: {msg.name}", expanded=False) as s:
                st.write(f"Tool Output:")
                st.code(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        st_callback = get_streamlit_cb(st.container())
        response = st.session_state.loop.run_until_complete(st.session_state.graph.invoke_graph(st.session_state.messages, st.session_state.config, [st_callback]))
        last_msg = response["messages"][-1]
        st.session_state.messages.append(AIMessage(last_msg.content))