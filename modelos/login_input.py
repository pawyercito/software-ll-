from pydantic import BaseModel

class LoginInput(BaseModel):
    correo: str
    contraseña: str