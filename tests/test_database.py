from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv('.env.test')

database_url = os.getenv("TEST_DATABASE_URL")

engine = create_engine(database_url)
TestLocalSession = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

