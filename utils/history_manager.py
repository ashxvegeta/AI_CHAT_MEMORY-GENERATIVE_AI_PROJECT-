from langchain_core.messages import HumanMessage, AIMessage
#history will be stored as a list of these objects.
from typing import List
# These prefixes help you understand who sent which message when loading them back.
HUMAN_PREFIX = "Human: "
AI_PREFIX = "AI: "

# This function reads your text file where chat history is stored
# and converts each line back into proper LangChain message objects
def load_chat_history(path: str="chat_history.txt")-> List[HumanMessage | AIMessage]:
    # ceeate a empty list to stroe the messahes
    history = []
    try:
        # llop though esach line in the file Remove \n from the end. 
        with open (path,"r",encoding="utf-8") as f:
            for lines in f:
                line = lines.strip("\n")
                if not line:
                    continue
                # Check the prefix to determine message type 
                # if a line starts with HUMAN_PREFIX, create a HumanMessage
                # if it starts with AI_PREFIX, create an AIMessage
                if line.startswith(HUMAN_PREFIX):
                    text = line[len(HUMAN_PREFIX):]
                    history.append(HumanMessage(content=text))
                # elif for AI message
                elif line.startswith(AI_PREFIX):
                    text = line[len(AI_PREFIX):]
                    history.append(AIMessage(content=text))
                # else just in case there is a line without prefix, treat it as human message
                else:
                    history.append(HumanMessage(content=line))

    # Handle the case where the file does not exist yet 
    # simply return an empty history list
    except FileNotFoundError:
        pass
    # Finally return the list of HumanMessage+AIMessage objects.
    return history
   
def  save_message(role:str,content:str,path:str="chat_history.txt")->None:
    # Determine the correct prefix based on the role
    if role == "human":
        prefix = HUMAN_PREFIX
    elif role == "ai":
        prefix = AI_PREFIX
    else:
        raise ValueError("Role must be either 'human' or 'ai'.")

    # Open the file in append mode and write the message with its prefix
    with open (path,"a",encoding="utf-8") as f:
        f.write(f"{prefix}{content}\n")