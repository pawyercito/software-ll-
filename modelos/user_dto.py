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

class UserResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    correo: str
    numero_telefonico: str
    contraseña: str
    message: str = "User found" # Proporcionar un valor predeterminado para el campo message

    class Config:
        orm_mode = True
        from_attributes=True

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

    class Config:
        orm_mode = True
        from_attributes=True

