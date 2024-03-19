from pydantic import BaseModel

class UserBase(BaseModel):
    nombre: str
    apellido: str
    correo: str
    numero_telefonico: str
    contraseña: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True