from modelos import user_dto as schemas
from repository import user_repository as repositories
from fastapi import HTTPException, status
import bcrypt

class UserUseCase:
    def __init__(self, user_repository: repositories.UserRepository):
        self.user_repository = user_repository

    def create_user(self, user: schemas.UserCreate):
        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(user.contraseña.encode(), bcrypt.gensalt())
        # Crear una copia del objeto user con la contraseña hasheada
        user_with_hashed_password = user.copy(update={"contraseña": hashed_password.decode()})
        return self.user_repository.create_user(user_with_hashed_password)
    