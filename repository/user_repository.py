from sqlalchemy.orm import Session
from modelos import user_model as models 
from modelos import user_dto as schemas
from modelos.user_dto import UserResponse
import bcrypt

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: schemas.UserCreate):
        db_user = models.User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_user_by_email(self, correo: str):
        user = self.db.query(models.User).filter(models.User.correo == correo).first()
        if user:
            # Crear la instancia de UserResponse usando from_orm
            user_response = UserResponse.from_orm(user)
            # Luego llamar a dict() en la instancia de UserResponse
            user_response_dict = user_response.dict()
            user_response_dict["message"] = "User found" # Añadir el mensaje manualmente
            return user_response_dict
        else:
            return None
            