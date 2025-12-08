from sqlalchemy import Column, Integer, String
from database import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)     # "human" or "ai"
    content = Column(String)
