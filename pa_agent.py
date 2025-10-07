# from dotenv import load_dotenv
# load_dotenv()

import os

import streamlit as st
from langgraph.graph import START, END

from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_google_community import GmailToolkit

import config as cfg
from mystate import MyState
from db import get_sqlite_conn, get_distinct_thread_ids
from llms import llm_gemini
from logger_config import get_logger 
from my_tools import get_tools
logger = get_logger()

class MyGraph():

    def __init__(self):
        self.llm = llm_gemini
        self.llm_with_tools = None
        self.tools_binded = False
        self.memory = None
        self.gmail_token = None
        self.graph = None
    
    async def build_graph(self):
        try:
            mem = await get_sqlite_conn()
            self.memory = AsyncSqliteSaver(mem)
            graph_builder = StateGraph(MyState)
            if self.gmail_token:
                tools = await get_tools(self.gmail_token)
            else:
                tools = await get_tools()
            toolnode = ToolNode(tools=tools)
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
        except Exception as e:
            logger.exception(e)

    async def get_history(self):
        try:
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
        except Exception as e:
            logger.exception(e)
   
    async def get_chat_block(self, config):
        return await self.graph.aget_state(config)
    
    async def rebuild_graph(self, gmail_token):
        self.gmail_token = gmail_token
        await self.build_graph()

    async def chatbot(self, state: MyState):
        if self.tools_binded:
            return {"messages": self.llm_with_tools.invoke(state["messages"])}
        else:
            return {"messages": self.llm.invoke(state["messages"])}

    async def invoke_graph(self, messages, config, callbacks):
        if callbacks: 
            config["callbacks"] = callbacks
        container = st.container()  # This container will hold the dynamic Streamlit UI components
        thoughts_placeholder = container.container()
        to_do_placeholder = thoughts_placeholder.empty()  # Container for displaying status messages
        token_placeholder = container.empty()  # Placeholder for displaying progressive token updates
        final_text = ""  # Will store the accumulated text from the model's response
        async for event in self.graph.astream_events({"messages": messages}, config):
            try: 
                kind = event["event"] # Determine the type of event received
                if event['name'] in ('write_todos', 'read_todos'):
                        continue  
                if kind == "on_chat_model_stream":
                    # The event corresponding to a stream of new content (tokens or chunks of text)
                    addition = event["data"]["chunk"].content  # Extract the new content chunk
                    final_text += addition  # Append the new content to the accumulated text
                    if addition:
                        token_placeholder.write(final_text)  # Update the st placeholder with the progressive response
                elif kind == "on_tool_start":
                    # The event signals that a tool is about to be called
                    with thoughts_placeholder:
                        status_placeholder = st.empty()  # Placeholder to show the tool's status
                        with status_placeholder.status("Calling Tool...", expanded=True) as s:
                            st.write("Called ", event['name'])  # Show which tool is being called
                            st.write("Tool input: ")
                            st.code(event['data'].get('input'))  # Display the input data sent to the tool
                            st.write("Tool output: ")
                            output_placeholder = st.empty()  # Placeholder for tool output that will be updated later below
                            s.update(label="Completed Calling Tool!", expanded=False)  # Update the status once done
                elif kind == "on_tool_end":
                    # The event signals the completion of a tool's execution
                    with thoughts_placeholder:
                        # We assume that `on_tool_end` comes after `on_tool_start`, meaning output_placeholder exists
                        if 'output_placeholder' in locals():
                            output_placeholder.code(event['data'].get('output').content)  # Display the tool's output
                elif kind == "on_custom_event":
                    if event["name"] == "on_todo_update":
                        with to_do_placeholder.status('TO-DO', expanded=True):
                            todos = event['data']['todo']
                            for task in todos:
                                if task["status"] == "pending":
                                    st.markdown(f"- [ ] {task['content']}")
                                elif task["status"] == "in_progress":
                                    st.markdown(f"🔄 **{task['content']}**")
                                elif task["status"] == "completed":
                                    st.markdown(f"- [x] ~~{task['content']}~~")
            except Exception as e:
                logger.exception(e)
        return final_text
         