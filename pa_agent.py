from dotenv import load_dotenv
load_dotenv()

import os

import streamlit as st
from langgraph.graph import START, END

# from langchaingoogle_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_google_community import GmailToolkit

import config as cfg
from mystate import MyState
from db import get_sqlite_conn
from llm_openai import llm_openai

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from langchain_mcp_adapters.client import MultiServerMCPClient 


class MyGraph():

    def __init__(self, gmail_token=None):
        self.llm = llm_openai
        self.llm_with_tools = None
        self.tools_binded = False
        # self.conn = get_sqlit_conn()
        self.memory = None
        self.gmail_token = gmail_token
        self.graph = None
    

    async def build_graph(self):
        mem = await get_sqlite_conn()
        self.memory = AsyncSqliteSaver(mem)
        graph_builder = StateGraph(MyState)
        if self.gmail_token:
            creds = Credentials(    
                token=self.gmail_token["access_token"],
                client_id=os.getenv("CLIENT_ID"),
                client_secret=os.getenv("CLIENT_SECRET"),
            )
            api_resource = build('gmail', 'v1', credentials=creds)
            toolkit = GmailToolkit(api_resource=api_resource)
            client = MultiServerMCPClient(
                {
                "F1_MCP": {
                    "url": "http://localhost:8000/mcp",
                    "transport": "streamable_http",
                    }
                }
            )
            tools =  st.session_state.loop.run_until_complete(client.get_tools())
            toolnode = ToolNode(tools)
            self.llm_with_tools = self.llm.bind_tools(tools)
            graph_builder.add_node("chatbot", self.chatbot)
            graph_builder.add_node("tools", toolnode)
            graph_builder.add_edge(START, "chatbot")
            graph_builder.add_conditional_edges("chatbot", tools_condition, path_map={
                "tools": "tools",
                END: END
            })
            self.tools_binded = True
            graph_builder.add_edge("tools", "chatbot")
            self.graph = graph_builder.compile(checkpointer=self.memory)
        else:
            graph_builder.add_node("chatbot", self.chatbot)
            graph_builder.add_edge(START, "chatbot")
            graph_builder.add_edge("chatbot", END)
            self.graph = graph_builder.compile(checkpointer=self.memory)
    
    async def get_chat_block(self, config):
        return await self.graph.aget_state(config)
    
    def rebuild_graph(self, gmail_token):
        self.gmail_token = gmail_token
        st.session_state.loop.run_until_complete(self.build_graph())

    def chatbot(self, state: MyState):
        if self.tools_binded:
            return {"messages": self.llm_with_tools.invoke(state["messages"])}
        else:
            return {"messages": self.llm.invoke(state["messages"])}

    async def invoke_graph(self, messages, config, callbacks):
        if callbacks: 
            config["callbacks"] = callbacks
        response = await self.graph.ainvoke({"messages": messages}, config)
        return response