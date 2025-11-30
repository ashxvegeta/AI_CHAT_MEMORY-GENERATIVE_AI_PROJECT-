# utils/history_manager.py
from langchain_core.messages import HumanMessage, AIMessage
from typing import List

HUMAN_PREFIX = "Human: "
AI_PREFIX = "AI: "

def load_chat_history(path: str = "chat_history.txt") -> List:
    history = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line:
                    continue
                if line.startswith(HUMAN_PREFIX):
                    text = line[len(HUMAN_PREFIX):]
                    history.append(HumanMessage(content=text))
                elif line.startswith(AI_PREFIX):
                    text = line[len(AI_PREFIX):]
                    history.append(AIMessage(content=text))
                else:
                    # fallback: treat as human message if no prefix
                    history.append(HumanMessage(content=line))
    except FileNotFoundError:
        # no previous history
        pass
    return history

def save_message(role: str, content: str, path: str = "chat_history.txt") -> None:
    prefix = HUMAN_PREFIX if role.lower() == "human" else AI_PREFIX
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{prefix}{content}\n")
