# app.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from utils.history_manager import load_chat_history, save_message

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY not found in environment. Add it to your .env file.")
    raise SystemExit(1)

# choose model you have access to; use gpt-3.5-turbo if gpt-4 is not available
MODEL_NAME = "gpt-4o-mini"  # change to "gpt-4" or "gpt-4o-mini" if you have access

model = ChatOpenAI(model=MODEL_NAME, temperature=0)

# Load previous chat history (list of HumanMessage / AIMessage)
chat_history = load_chat_history()

# Start with a system message defining assistant behaviour
system_msg = SystemMessage(content="You are a helpful AI assistant.")

print("=== AI Chatbot (type 'exit' to quit) ===")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ("exit", "quit"):
        print("Goodbye!")
        break

    # Build messages: system + existing history + new user message
    messages = [system_msg] + chat_history + [HumanMessage(content=user_input)]

    # Save user message to file & local list
    save_message("human", user_input)
    chat_history.append(HumanMessage(content=user_input))

    # Invoke the model with message list
    response = model.invoke(messages)
    reply_text = response.content.strip()

    # Print and save AI response
    print("AI:", reply_text)
    save_message("ai", reply_text)
    chat_history.append(AIMessage(content=reply_text))
