from fastapi import APIRouter

from app.ai.agent import ask_agent
from app.memory.conversation import create_conversation
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:

    conversation_id = request.conversation_id

    if conversation_id is None:
        conversation_id = create_conversation()

    answer = ask_agent(
        conversation_id,
        request.message,
    )

    return ChatResponse(
        conversation_id=conversation_id,
        answer=answer,
    )