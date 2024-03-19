from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    correo = Column(String, unique=True, index=True)
    numero_telefonico = Column(String, index=True)
    contraseña = Column(String)