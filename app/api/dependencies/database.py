from sqlalchemy.orm import Session
from app.database import SessionLocal

# Dependency to get a database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
