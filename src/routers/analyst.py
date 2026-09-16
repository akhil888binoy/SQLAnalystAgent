
from fastapi import APIRouter, Depends, HTTPException
from langchain.messages import HumanMessage
from src.agent.agent import agent

analyst_router = APIRouter(
    prefix="/api/analyst",
    tags=["analyst"]
)


@analyst_router.post("/")
def get_analysis(request):

    messages = [HumanMessage(content=request)]

    result = agent.invoke({
        "messages": messages
    })

    for message in result["messages"]:
        message.pretty_print()

    return {
        "answer": result["messages"][-1].content
    }