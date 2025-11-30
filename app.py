# 1. Import all required modules
# to read environment variables
import os
# loads API key from .env
from dotenv import load_dotenv
# actual AI model class
from langchain_openai import ChatOpenAI
# required for creating chat messages
from langchain_core.messages import HumanMessage, AIMessage ,SystemMessage
# read memory from file and save new messages
from utils.history_manager import load_chat_history, save_message

# ✅ 2. Load the .env file
load_dotenv()

# ✅ 3. Check if API key exists
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Please set your OPENAI_API_KEY in a .env file")
    raise SystemExit(1) # Stop here if API key is missing

# ✅ 4. Select which OpenAI model to use
MODEL_NAME = "gpt-4o-mini" 
model = ChatOpenAI(model_name=MODEL_NAME,temperature=0)

# ✅ 5. Load chat memory from file
chat_history = load_chat_history()  #This function reads chat_history.txt and returns a list like:

# ✅ 6. Create the system message
# This message ALWAYS stays at the top.
# It defines how the AI should behave.
system_message = SystemMessage(content="You are a helpful AI assistant.")


# ✅ 7. Start the chatbot loop
print("=== AI Chatbot (type 'exit' to quit) ===")


while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    # ✅ 8. If user types "exit", quit
    if user_input.lower() == "exit":
        print("Exiting chat. Goodbye!")
        break

    # ✅ 9. Build the message list to send to model
     # Build messages: system + existing history + new user message
    messages = [system_message] + chat_history + [HumanMessage(content=user_input)]

    # ✅ 10. Save the new HUMAN message
    # Save user message to file & local list
    #  Writes into chat_history.txt
    # Adds the message to in-memory list
    save_message("human",user_input)
    chat_history.append(HumanMessage(content=user_input))

    # ✅ 11. Call the AI model
    #invoke the model to get AI response
    response = model.invoke(messages)
    reply_text  = response.content.strip()

    # ✅ 12. Print & save AI’s response
    # Print and save AI response
    print("AI:" , reply_text)
    save_message("ai",reply_text)
    chat_history.append(AIMessage(content=reply_text))
