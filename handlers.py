from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi import Response
from modelos import user_dto as schemas
from use_case import user_use_case as use_cases
from repository import user_repository as repositories
from database import SessionLocal
from fastapi import HTTPException, status
from modelos import login_dto as login_schemas
from repository.user_repository import UserRepository
from use_case.login_use_case import LoginUseCase
from modelos.login_input import LoginInput
from repository.cita_repository import CitaRepository
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from modelos import additional_info_dto as additional_info_schemas


from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from use_case.citas_use_case import AgendarCitaUseCase

from fastapi.staticfiles import StaticFiles

from modelos import citas_dto_model as citas_schemas

from modelos.additional_info_dto import AdditionalInfoDTO

import logging


from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode, PyJWTError
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from utils.get_doctor_info import obtener_nombre_especialidad_doctores

from modelos.user_model import User

from fastapi.responses import JSONResponse

from typing import Optional

import logging

from datetime import timedelta
# Configurar el nivel de logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Crear un logger
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from fastapi import Header

def get_current_user(db: Session = Depends(get_db), token: str = Header(None, alias="Authorization")) -> Optional[User]:
    if token is None:
        logger.error("Token not received")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Remove the "Bearer " prefix from the token
        token = token.replace("Bearer ", "")
        logger.debug(f"Received token: {token}")

        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Decoded payload: {payload}")

        user_id: int = payload.get("sub")
        if user_id is None:
            logger.error("User ID not found in the token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            logger.error(f"User with ID {user_id} not found in the database")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.debug(f"Retrieved user: {user}")
        return user

    except PyJWTError as e:
        logger.error(f"Error decoding the token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


templates = Jinja2Templates(directory="templates")

SECRET_KEY = "1234567897421231578942315798"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter()


router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/users/", response_class=HTMLResponse)
def render_registration_form(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@router.post("/users/", response_model=schemas.User)
def create_user(
    nombre: str = Form(...),
    apellido: str = Form(...),
    correo: str = Form(...),
    numero_telefonico: str = Form(...),
    contraseña: str = Form(...),
    db: Session = Depends(get_db)
):
    user_data = schemas.UserCreate(
        nombre=nombre,
        apellido=apellido,
        correo=correo,
        numero_telefonico=numero_telefonico,
        contraseña=contraseña
    )
    user_use_case = use_cases.UserUseCase(repositories.UserRepository(db))
    user_created = user_use_case.create_user(user_data)
    return user_created

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

@router.get("/login", response_class=HTMLResponse)
def render_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
logger.error("Iniciando la función de login")
@router.post("/login", response_model=schemas.Token)
def login(
    correo: str = Form(...),
    contraseña: str = Form(...),
    user_repository: UserRepository = Depends(get_user_repository)
    
):
    logger.error("Iniciando la función de login")
    logger.debug(f"Iniciando el proceso de login para el correo: {correo}") # Log del inicio del proceso de login
    login_use_case = LoginUseCase(user_repository)
    user_id = login_use_case.execute(correo, contraseña)
    if user_id:
        logger.debug(f"Usuario encontrado con ID: {user_id}") # Log del usuario encontrado
        # Generar el token JWT
        token_data = {"sub": user_id}
        token = encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        logger.debug(f"Token generado: {token}") # Log del token generado
        token_expiration = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return {"access_token": token, "token_type": "bearer", "expires_in": int(token_expiration.total_seconds())}
        
    else:
        logger.debug(f"No se encontró un usuario con el correo: {correo}") # Log cuando no se encuentra un usuario
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
@router.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("inicio.html", {"request": request})


def get_cita_repository(db: Session = Depends(get_db)):
    return CitaRepository(db)

@router.post("/citas/", response_model=citas_schemas.Cita)
def agendar_cita(
    doctor: str = Form(...),
    especialidad: str = Form(...),
    fecha: str = Form(...),
    user: User = Depends(get_current_user), # Asegúrate de que esta línea esté presente
    cita_repository: CitaRepository = Depends(get_cita_repository)
):
    agendar_cita_use_case = AgendarCitaUseCase(cita_repository)
    cita = agendar_cita_use_case.execute(doctor, especialidad, fecha, user.id)  # Usa user.nombre
    cita.nombre = user.nombre  # Asigna el nombre del usuario a la cita
    return cita


@router.get("/citas/", response_class=HTMLResponse)
def citas(request: Request, db: Session = Depends(get_db)):
    doctores = obtener_nombre_especialidad_doctores(db)
    return templates.TemplateResponse("agendar_citas.html", {"request": request, "doctores": doctores})
    

@router.get("/perfil/", response_class=HTMLResponse)
def perfil(request: Request, user: User = Depends(get_current_user), cita_repository: CitaRepository = Depends(get_cita_repository)):
    # Obtiene la información adicional del usuario
    additional_info = user.additional_info
    additional_info_dto = AdditionalInfoDTO(**additional_info.__dict__)

    # Obtiene las citas agendadas por el usuario
    citas_agendadas = cita_repository.get_citas_by_user(user.id)

    # Pasa la información del usuario y las citas agendadas al template
    return templates.TemplateResponse("perfil.html", {
        "request": request,
        "user": user,
        "additional_info": additional_info_dto,
        "citas_agendadas": citas_agendadas,
    })