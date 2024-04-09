# modelos/additional_info_dto.py
from pydantic import BaseModel
from datetime import date

class AdditionalInfoDTO(BaseModel):
    direccion: str
    telefono: str
    sexo: str
    fecha_nacimiento: date
    user_id: int 