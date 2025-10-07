from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from typing import Annotated
from mystate import Todo

from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from my_prompts import WRITE_TODOS_TOOL_DESCRIPTION
from langchain_google_community import GmailToolkit
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import config as cfg
import json
import os
from langchain.tools.retriever import create_retriever_tool
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings


from mystate import MyState

from langchain_core.callbacks import adispatch_custom_event

from langchain_mcp_adapters.client import MultiServerMCPClient 

from datetime import datetime

tavily_search = TavilySearch(
    max_results = 5
)

@tool(description=WRITE_TODOS_TOOL_DESCRIPTION)
async def write_todos(
    todos: list[Todo], tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    await adispatch_custom_event( 
        name="on_todo_update",
        data={
            "todo": todos
        }
    )
    return Command(
        update={
            "todos": todos,
            "messages": [
                ToolMessage(f"Updated todo list to {todos}", tool_call_id=tool_call_id)
            ],
        }
    )

@tool()
async def read_todos(state: Annotated[MyState, InjectedState]):
    """Read the current TODO list from the agent state.

    This tool allows the agent to retrieve and review the current TODO list
    to stay focused on remaining tasks and track progress through complex workflows.

    Args:
        state: Injected agent state containing the current TODO list
        tool_call_id: Injected tool call identifier for message tracking

    Returns:
        Formatted string representation of the current TODO list
    """

    todos = state.get("todos", [])
    if not todos:
        return "No todos currently in the list."

    result = "Current TODO List:\n"
    for i, todo in enumerate(todos, 1):
        status_emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}
        emoji = status_emoji.get(todo["status"], "❓")
        result += f"{i}. {emoji} {todo['content']} ({todo['status']})\n"

    return result.strip()

@tool()
async def date_tool():
    """
    Returns the current date/time
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d")

async def get_tools(gmail_token = None):
    gmail_tools = []
    with open(cfg.RETRIEVER_STATUS_FILE, 'r') as f:
        retriever_status = json.load(f)
    description = ""
    for pdf, info in retriever_status.items():
        if info["status"] == "Done":
            description += f'{info["description"]}' + "\n"
    if gmail_token:
        creds = Credentials(    
                    token=gmail_token["access_token"],
                    refresh_token=gmail_token["refresh_token"],
                    client_id=os.getenv("CLIENT_ID"),
                    client_secret=os.getenv("CLIENT_SECRET"),
                )
        api_resource = build('gmail', 'v1', credentials=creds)
        toolkit = GmailToolkit(api_resource=api_resource)
        gmail_tools = toolkit.get_tools()
    mcp_client = MultiServerMCPClient(
        cfg.MCP_CONFIG
    )
    f1_tools = await mcp_client.get_tools()
    chromadb = Chroma( 
            collection_name=cfg.VEC_COLLECTION_NAME,
            embedding_function=GoogleGenerativeAIEmbeddings(model=cfg.VEC_EMBEDDING_NAME),
            persist_directory=cfg.VEC_DB_PATH
        )
    retriever = chromadb.as_retriever(
                search_kwargs = {"k": 5}
            )
    retriever_tool = create_retriever_tool( 
                retriever= retriever,
                name='retriever_health_blog_post',
                description=description
            )
    return [
        tavily_search, read_todos, write_todos, retriever_tool, date_tool
    ] + gmail_tools + f1_tools