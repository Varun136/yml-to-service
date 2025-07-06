from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import HumanMessage, AIMessage

class AgentState(TypedDict):
        messages: Annotated[list, add_messages]


class DeveloperAgent:

    def __init__(self):
        self._graph: Optional[CompiledStateGraph] = None
        self._memmory: Optional[dict] = None

        # Initiaise the graph
        self._initialise()

    def _agent_node(self, state: AgentState) -> str:
        """
        Example agent node that processes messages.
        """
        # Here you would implement your agent logic.
        return {"messages": [AIMessage("Agent processed the messages.")]}

    def _initialise(self):
        if self._graph:
            return 
        graph_builder = StateGraph(AgentState)
        graph_builder.add_node("agent_node", self._agent_node)

        graph_builder.add_edge(START, "agent_node")
        graph_builder.add_edge("agent_node", END)
        self._graph = graph_builder.compile()
        
    async def run(self, project_details: str) -> str:
        if not self._graph:
            raise RuntimeError("Graph not initialized.")
        
        user_message = [HumanMessage(content=project_details)]
        response = self._graph.invoke({"messages": user_message})
        return response["messages"][0].content