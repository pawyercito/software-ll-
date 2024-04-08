from pydantic import BaseModel
from datetime import date
from modelos.user_dto import UserBase
from typing import Optional

class CitaBase(BaseModel):
    doctor: str
    especialidad: str
    fecha: date
    user: Optional[UserBase] = None  # Hacer que el campo user sea opcional

class CitaCreate(CitaBase):
    pass

class Cita(CitaBase):
    id: int
    nombre: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes=True