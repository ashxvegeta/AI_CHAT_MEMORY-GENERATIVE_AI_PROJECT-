from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from utils.history_manager import load_chat_history, save_message

load_dotenv()

app = FastAPI()

# ✅ Load API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Load Model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ✅ Load previous chat memory
chat_history = load_chat_history()

# ✅ System message (bot behavior)
system_msg = SystemMessage(content="You are a helpful AI assistant.")

# ✅ Request body model
class ChatRequest(BaseModel):
    message: str


# ✅ Testing route
@app.get("/")
def home():
    return {"message": "AI Chatbot with Memory is Running!"}


# ✅ Main Chat API

@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.message

    # ✅ Reload memory fresh from file every request
    chat_history = load_chat_history()

    chat_history.append(HumanMessage(content=user_input))
    save_message("human", user_input)

    messages = [system_msg] + chat_history

    response = model.invoke(messages)
    reply_text = response.content.strip()

    chat_history.append(AIMessage(content=reply_text))
    save_message("ai", reply_text)

    return {
        "reply": reply_text,
        "history": [
            {"role": "human", "content": m.content}
            if isinstance(m, HumanMessage)
            else {"role": "ai", "content": m.content}
            for m in chat_history
        ]
    }