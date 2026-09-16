from fastapi import APIRouter
from pydantic import BaseModel
from langchain.messages import HumanMessage
from src.agent.agent import agent

analyst_router = APIRouter(
    prefix="/api/analyst",
    tags=["analyst"]
)


class AnalysisRequest(BaseModel):
    question: str


@analyst_router.post("/")
def get_analysis(request: AnalysisRequest):
    result = agent.invoke({
        "messages": [HumanMessage(content=request.question)]
    })

    return {
        "answer": result["messages"][-1].content
    }
