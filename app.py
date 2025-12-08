from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from database import SessionLocal, engine, Base
from models import Chat

load_dotenv()

# ✅ Create DB Tables
Base.metadata.create_all(bind=engine)

# ✅ Create FastAPI App
app = FastAPI()

# ✅ Enable Frontend Access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:  
    raise RuntimeError("OPENAI_API_KEY is not set in environment variables.")

# ✅ Load Model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ✅ System message
system_msg = SystemMessage(content="You are a helpful AI assistant.")

# ✅ Request Body
class ChatRequest(BaseModel):
    message: str


# ✅ Health Check
@app.get("/health")
def health():
    return {"status": "Server is running."}


# ✅ MAIN CHAT API (DATABASE)
@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.message.strip()
    if not user_input:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    db = SessionLocal()

    try:
        # ✅ Load Previous Chat from DB
        chats = db.query(Chat).all()

        chat_history = []
        for chat in chats:
            if chat.role == "human":
                chat_history.append(HumanMessage(content=chat.content))
            else:
                chat_history.append(AIMessage(content=chat.content))

        # ✅ Save User Message
        db.add(Chat(role="human", content=user_input))
        db.commit()

        chat_history.append(HumanMessage(content=user_input))

        # ✅ Send to AI
        messages = [system_msg] + chat_history
        response = model.invoke(messages)
        reply_text = response.content.strip()

        # ✅ Save AI Reply
        db.add(Chat(role="ai", content=reply_text))
        db.commit()

        chat_history.append(AIMessage(content=reply_text))

        return {
            "reply": reply_text,
            "history": [
                {"role": "human", "content": msg.content}
                if isinstance(msg, HumanMessage)
                else {"role": "ai", "content": msg.content}
                for msg in chat_history
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


# ✅ GET FULL CHAT HISTORY
@app.get("/history")
def get_history():
    db = SessionLocal()
    try:
        chats = db.query(Chat).all()
        return {
            "history": [
                {"role": chat.role, "content": chat.content}
                for chat in chats
            ]
        }
    finally:
        db.close()


# ✅ CLEAR CHAT HISTORY
@app.get("/clear_history")
def clear_history():
    db = SessionLocal()
    try:
        db.query(Chat).delete()
        db.commit()
        return {"status": "Chat history cleared from database"}
    finally:
        db.close()
