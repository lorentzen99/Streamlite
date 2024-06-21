from sqlalchemy.orm import Session
from app.api.models.user import User
from app.api.schemas.user import UserCreate, UserUpdate
from app.api.crud.crud import CRUDGeneric


class CRUDUser(CRUDGeneric[User, UserCreate, UserUpdate]):
    def __init__(self, model: User):
        super().__init__(model)

    def get_by_username(self, db: Session, username: str) -> User:
        return db.query(self.model).filter(self.model.username == username).first()
