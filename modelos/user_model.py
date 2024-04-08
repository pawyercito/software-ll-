from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    correo = Column(String, unique=True, index=True)
    numero_telefonico = Column(String, index=True)
    contraseña = Column(String)

    citas = relationship("Cita", back_populates="user")


# Agregar esta línea para acceder a los datos de la nueva tabla desde la tabla "users"
    additional_info = relationship("AdditionalInfo", back_populates="user")

class AdditionalInfo(Base):
    __tablename__ = "additional_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="additional_info")

    # Nuevas columnas
    direccion = Column(String, index=True)
    telefono = Column(String, index=True)
    sexo = Column(String, index=True)
    fecha_nacimiento = Column(Date)