from dotenv import load_dotenv
load_dotenv()

import os


from langgraph.graph import START, END

# from langchaingoogle_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_google_community import GmailToolkit

import config as cfg
from mystate import MyState
from db import get_sqlit_conn
from llm_openai import llm_openai

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from langchain_mcp_adapters.client import MultiServerMCPClient 

client = {
    "F1_MCP": {
        "url": "http://localhost:8000/mcp/",
        "transport": "sse",
    }
}

class MyGraph():

    def __init__(self, gmail_token=None):
        self.llm = llm_openai
        self.llm_with_tools = None
        self.tools_binded = False
        self.conn = get_sqlit_conn()
        self.memory = SqliteSaver(self.conn)
        self.gmail_token = gmail_token
        self.graph = self._build_graph()
        

    def _build_graph(self):

        graph_builder = StateGraph(MyState)
        if self.gmail_token:
            creds = Credentials(    
                token=self.gmail_token["access_token"],
                client_id=os.getenv("CLIENT_ID"),
                client_secret=os.getenv("CLIENT_SECRET"),
            )
            api_resource = build('gmail', 'v1', credentials=creds)
            toolkit = GmailToolkit(api_resource=api_resource)
            toolnode = ToolNode(toolkit.get_tools())
            self.llm_with_tools = self.llm.bind_tools(toolkit.get_tools())
            graph_builder.add_node("chatbot", self.chatbot)
            graph_builder.add_node("tools", toolnode)
            graph_builder.add_edge(START, "chatbot")
            graph_builder.add_conditional_edges("chatbot", tools_condition, path_map={
                "tools": "tools",
                END: END
            })
            self.tools_binded = True
            graph_builder.add_edge("tools", "chatbot")
            mygraph = graph_builder.compile(checkpointer=self.memory)
            return mygraph
        else:
            graph_builder.add_node("chatbot", self.chatbot)
            graph_builder.add_edge(START, "chatbot")
            graph_builder.add_edge("chatbot", END)
            mygraph = graph_builder.compile(checkpointer=self.memory)
            return mygraph
    
    def rebuild_graph(self, gmail_token):
        self.gmail_token = gmail_token
        self.graph = self._build_graph()

    def chatbot(self, state: MyState):
        if self.tools_binded:
            return {"messages": self.llm_with_tools.invoke(state["messages"])}
        else:
            return {"messages": self.llm.invoke(state["messages"])}

    def invoke_graph(self, messages, config, callbacks):
        if callbacks: 
            config["callbacks"] = callbacks
        response = self.graph.invoke({"messages": messages}, config)
        return response