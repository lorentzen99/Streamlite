from sqlalchemy.orm import Session
from app.api.models.user import User
from app.api.schemas.user import UserCreate, UserUpdate
from app.api.crud.crud import CRUDGeneric


class CRUDUser(CRUDGeneric[User, UserCreate, UserUpdate]):
    def __init__(self, model: User):
        super().__init__(model)

    def get(self, db: Session, user_id: int) -> User:
        return super().get(db, user_id)

    def get_by_username(self, db: Session, username: str) -> User:
        return db.query(self.model).filter(self.model.username == username).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 10) -> list:
        return super().get_multi(db, skip, limit)
    
    def create(self, db: Session, user: UserCreate) -> User:
        return super().create(db, user)
    
    def update(self, db: Session, user_id: int, user: UserUpdate) -> User:
        return super().update(db, user_id, user)
    
    def delete(self, db: Session, user_id: int) -> User:
        return super().delete(db, user_id)


crud_user = CRUDUser(User)
