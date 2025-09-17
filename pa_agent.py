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
from db import get_sqlite_conn, get_distinct_thread_ids
from llm_openai import llm_gemini

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from langchain_mcp_adapters.client import MultiServerMCPClient 

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.tools.retriever import create_retriever_tool


class MyGraph():

    def __init__(self, gmail_token=None):
        self.llm = llm_gemini
        self.llm_with_tools = None
        self.tools_binded = False
        # self.conn = get_sqlit_conn()
        self.memory = None
        self.gmail_token = gmail_token
        self.graph = None
        self.chromadb = Chroma( 
            collection_name="banner_health_blogs",
            embedding_function=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001"),
            persist_directory=cfg.VEC_DB_PATH
        )
    
    async def get_history(self):

        chats = []
        threads = await get_distinct_thread_ids()
        for thread in threads:
            conf = {"configurable": {"thread_id": thread}}
            block = await self.memory.aget(conf)
            history = block["channel_values"]["messages"]
            if len(history) > 3:
                chats.append(
                    {
                        "thread_id": thread,
                        "message" : history[2]
                    }
                )
            elif len(history) > 2:
                chats.append(
                    {
                        "thread_id": thread,
                        "message" : history[1]
                    }
                )
            else:
                chats.append(
                    {
                        "thread_id": thread,
                        "message" : "New chat"
                    }
                )    
        return chats        
    

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
            gmail_tools = toolkit.get_tools()
            client = MultiServerMCPClient(
                {
                "F1_MCP": {
                    "url": "http://localhost:8000/mcp",
                    "transport": "streamable_http",
                    }
                }
            )
            f1_tools =  st.session_state.loop.run_until_complete(client.get_tools())
            
            retriever = self.chromadb.as_retriever(
                search_kwargs = {"k": 5}
            )

            retriever_tool = create_retriever_tool( 
                retriever= retriever,
                name='retriever_health_blog_post',
                description="""
                Search and return documents relevant to
                1.) How to beat afternoon slump by boosting energy
                2.) How to manage carvings
                3.) what to do about loctose_intolerance
                """
            )

            toolnode = ToolNode(gmail_tools + f1_tools + [retriever_tool])
            self.llm_with_tools = self.llm.bind_tools(gmail_tools + f1_tools + [retriever_tool])
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
    
    # def flow_decider(self, state: MyState):
    #     if messages := state.get("messages", []):
    #         ai_message = messages[-1]
    #     if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
    
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