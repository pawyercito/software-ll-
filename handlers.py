from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modelos import user_dto as schemas
from use_case import user_use_case as use_cases
from repository import user_repository as repositories
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_use_case = use_cases.UserUseCase(repositories.UserRepository(db))
    return user_use_case.create_user(user)