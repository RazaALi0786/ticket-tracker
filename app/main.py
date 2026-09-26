from fastapi import FastAPI

from app.ai.model import model
from app.database.connection import Base, engine
from app.database.models import Conversation, Message, Ticket
from app.routes.chat import router as chat_router


Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Customer Support Agent API is running"
    }

app.include_router(chat_router)

@app.get("/gemini-test")
def gemini_test():
    response = model.invoke(
        "My device won't turn on. What should I do?"
    )

    return {
        "response": response.text
    }