from fastapi import HTTPException, status
from repository.user_repository import UserRepository
from modelos.user_dto import UserResponse
import bcrypt

class LoginUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str, contraseña: str):
        user = self.user_repository.get_user_by_email(email)
        if user and bcrypt.checkpw(contraseña.encode(), user["contraseña"].encode()):
            return user["id"] # Devuelve el ID del usuario
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )