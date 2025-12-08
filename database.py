
# create_engine	Connects Python to the database	🔌 Database wire
# sessionmaker	Creates a database session	🧑‍💼 DB worker
# declarative_base	Creates base for all tables	🏗️ Table foundation

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# The database URL for SQLite  chat.db file automatically created in the current directory.
DATABASE_URL = "sqlite:///./chat.db"

# This actually opens the connection to the database.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Creates a configured "Session" class

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Create the Base for All Tables 
Base = declarative_base()
