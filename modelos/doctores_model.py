from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class Doctor(Base):
    __tablename__ = "doctores"

    id_doctor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    especialidad = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True)
    numero_telefonico = Column(String, index=True)
    contraseña = Column(String)
    fecha_nacimiento = Column(Date, nullable=False)
      

