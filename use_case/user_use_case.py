from modelos import user_dto as schemas
from repository import user_repository as repositories

class UserUseCase:
    def __init__(self, user_repository: repositories.UserRepository):
        self.user_repository = user_repository

    def create_user(self, user: schemas.UserCreate):
        return self.user_repository.create_user(user)