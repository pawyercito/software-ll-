from sqlalchemy.orm import Session
from modelos.doctores_model import Doctor # Asegúrate de importar el modelo Doctor correctamente

def obtener_nombre_especialidad_doctores(db: Session):
    doctores = db.query(Doctor.nombre, Doctor.especialidad).all()
    return doctores