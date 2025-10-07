from typing import Annotated, List, Literal, NotRequired
from langgraph.graph import add_messages
from typing_extensions import TypedDict

class Todo(TypedDict):
    content: str 
    status : Literal["pending", "in_progress", "completed"]

class MyState(TypedDict):
    todos: NotRequired[List[Todo]]
    messages : Annotated[List, add_messages]