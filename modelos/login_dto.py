from pydantic import BaseModel

class UserLogin(BaseModel):
    correo: str
    contraseña: str

