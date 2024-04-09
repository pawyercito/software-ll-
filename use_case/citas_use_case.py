from repository.cita_repository import CitaRepository
from modelos import citas_model as models


class AgendarCitaUseCase:
    def __init__(self, cita_repository: CitaRepository):
        self.cita_repository = cita_repository

    def execute(self, doctor, especialidad, fecha, user_id):
        cita = models.Cita(doctor=doctor, especialidad=especialidad, fecha=fecha, user_id=user_id)
        return self.cita_repository.create_cita(cita)
    


class ObtenerCitasUseCase:
    def __init__(self, cita_repository: CitaRepository):
        self.cita_repository = cita_repository

    def execute(self, user_id):
        citas = self.cita_repository.get_citas_by_user(user_id)
        return citas