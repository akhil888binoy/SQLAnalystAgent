from src.tools.database import execute_sql
from src.tools.schema import get_schema
from langchain.messages import SystemMessage
from  src.agent.state import SQLAgentState
from langchain.messages import ToolMessage
import os
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="inclusionai/ling-3.0-flash-vl:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)   



tools = [execute_sql, get_schema ]
llm_with_tools = model.bind_tools(tools)
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)
 



def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))
    return {"messages": result}


def llm_call(state: SQLAgentState):
    """LLM decides whether to call a tool or not"""

    message = model_with_tools.invoke(
                [
                    SystemMessage(
                            content="""
                                You are a helpful SQL analyst working with a PostgreSQL database.

                                Always call get_schema first to discover tables and columns. Never query sqlite_master or other SQLite-specific catalogs.

                                Use the available database tools to answer the user's question accurately.

                                If a SQL execution returns an error:
                                1. Understand the error.
                                2. Inspect the schema if necessary.
                                3. Correct the SQL query.
                                4. Execute the corrected query.
                                5. Only provide the final answer after obtaining a valid result.
                                """
                            )
                ]
                + state["messages"]
            )

    #  OpenRouter's ling model sometimes returns list content it then rejects on resend; flatten to text
    if not isinstance(message.content, str):
        message.content = str(message.text)

    return {
        "messages": [message],
        "llm_calls": state.get('llm_calls', 0) + 1
    }