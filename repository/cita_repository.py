from sqlalchemy.orm import Session
from modelos import citas_model as models

class CitaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_cita(self, cita):
        self.db.add(cita)
        self.db.commit()
        self.db.refresh(cita)
        return cita

    def get_citas_by_doctor(self, doctor):
        return self.db.query(models.Cita).filter(models.Cita.doctor == doctor).all()
    
    def get_citas_by_user(self, user_id):
        return self.db.query(models.Cita).filter(models.Cita.user_id == user_id).all()
    
    
    