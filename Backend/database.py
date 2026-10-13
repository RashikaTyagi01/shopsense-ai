from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
import os 
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL=os.getenv("DATABASE_URL")
#engine = create_engine(DATABASE_URL, connect_args={"check_same_thread":False})
engine = create_engine(DATABASE_URL)

Base=declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

