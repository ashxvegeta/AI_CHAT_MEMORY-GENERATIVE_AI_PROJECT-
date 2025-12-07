from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from utils.history_manager import load_chat_history, save_message

load_dotenv()

# ✅ Create FastAPI app
app = FastAPI()

# ✅ Load API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:  
    raise RuntimeError("OPENAI_API_KEY is not set in environment variables.")

# ✅ Load Model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ✅ System message (bot behavior)
system_msg = SystemMessage(content="You are a helpful AI assistant.")


# ✅ Request body model
class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "Server is running."}

# ✅ Main Chat API

@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.message.strip()

    if not user_input:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    try:
      # ✅ Load memory fresh every request
        chat_history = load_chat_history()

        # ✅ Add user message to memory
        chat_history.append(HumanMessage(content=user_input))
        save_message("human", user_input)

        # ✅ Send messages to AI

        message =  [system_msg] + chat_history
        response = model.invoke(message)

        reply_text = response.content.strip()

        # ✅ Save AI reply
        chat_history.append(AIMessage(content=reply_text))
        save_message("ai", reply_text)


        return {"reply": reply_text,
                "history":[
                    {"role": "human", "content": msg.content} if isinstance(msg, HumanMessage) else
                    {"role": "ai", "content": msg.content} for msg in chat_history
                ]
                
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get Full Chat History
@app.get("/history")
def get_history():
    try:
        chat_history = load_chat_history()
        return {
            "history": [
                {"role": "human", "content": msg.content} if isinstance(msg, HumanMessage) else
                {"role": "ai", "content": msg.content} for msg in chat_history
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# ✅ Clear Chat History
@app.get("/clear_history")
def clear_history():
    try:
        if os.path.exists("chat_history.txt"):
            os.remove("chat_history.txt")
        return {"status": "Chat history cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))