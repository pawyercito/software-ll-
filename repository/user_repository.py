from sqlalchemy.orm import Session
from modelos import user_model as models 
from modelos import user_dto as schemas

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: schemas.UserCreate):
        db_user = models.User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user