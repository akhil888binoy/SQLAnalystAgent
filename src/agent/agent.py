
from src.agent.conditional import should_continue
from src.agent.state import SQLAgentState
from src.llm.llm import llm_call,tool_node
from langgraph.graph import StateGraph, START, END
from langchain.messages import HumanMessage




# Build workflow
agent_builder = StateGraph(SQLAgentState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")

agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_call")

# Compile the agent
agent = agent_builder.compile()

 