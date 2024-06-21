import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_username = os.getenv('STREAMLITE_DB_USERNAME')
db_password = os.getenv('STREAMLITE_DB_PASSWORD')
print("USERNAME: ", db_username) # TODO Remove print statements
print("PASSWORD: ", db_password)

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_username}:{db_password}@localhost:5433/streamlite"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
