import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import HumanMessage, SystemMessage
from tempfile import TemporaryDirectory
from langchain_openai import ChatOpenAI
from src.langgraph.tools import get_file_management_tools, zip_temp_dir
from langgraph.prebuilt import ToolNode
from src.langgraph.config import FileSystemAgent

load_dotenv(override=True)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    session_id: str


class DeveloperAgent:

    def __init__(self):
        self._graph: Optional[CompiledStateGraph] = None
        self._memmory: Optional[dict] = None
        self._work_dir: TemporaryDirectory = TemporaryDirectory()
        self._file_system_tools = get_file_management_tools(self._work_dir.name)

        self._file_system_model = ChatOpenAI(
            api_key=os.environ.get("API_KEY"),
            base_url=os.environ.get("BASE_URL"),
            model=FileSystemAgent.model
        ).bind_tools(self._file_system_tools)
        
        self._initialise()

    def _file_system_node(self, state: AgentState) -> str:
        """
        File System Agent:
            1. Creates the project strucutre, files and folders.
            2. Write the views, routes and other documents.
        """
        system_prompt = SystemMessage(FileSystemAgent.system_pompt)
        
        message = [system_prompt, *state["messages"]]
        response = self._file_system_model.invoke(message)

        return {"messages": response, "session_id": state["session_id"]}
    

    def _zip_tool_node(self, state: AgentState) -> dict:
        """Zips the temp project structure and saves it locally"""
        session_id = state["session_id"]

        zip_path = zip_temp_dir(self._work_dir.name, session_id)
        state["zip_path"] = zip_path
        self._work_dir.cleanup()
        return state
    

    def _conditional_node(self, state: AgentState):
        messages = messages = state.get("messages", [])
        if not messages:
            return "end"

        last_message = messages[-1]
        if last_message.additional_kwargs.get("tool_calls"):
            return "tool_node"
        else:
            return "zip"


    def _initialise(self):
        if self._graph:
            return 
        graph_builder = StateGraph(AgentState)
        graph_builder.add_node("file_system_node", self._file_system_node)

        tool_node = ToolNode(self._file_system_tools)
        graph_builder.add_node("tool_node", tool_node)

        graph_builder.add_node("zip_node", self._zip_tool_node)

        graph_builder.add_edge(START, "file_system_node")
        graph_builder.add_conditional_edges(
            "file_system_node", 
            self._conditional_node, 
            {
                "tool_node": "tool_node",
                "zip": "zip_node",
                "end": END
            }
        )
        graph_builder.add_edge("tool_node", "file_system_node")
        graph_builder.add_edge("zip_node", END)
        self._graph = graph_builder.compile()
    

    async def run(self, service: str, session_id: str) -> str:
        if not self._graph:
            raise RuntimeError("Graph not initialized.")
        message = {
        "messages": [HumanMessage(f"Create a project structure for a {service}")],
        "session_id": session_id
        }
        response = self._graph.invoke(message)
        return response["messages"][0].content