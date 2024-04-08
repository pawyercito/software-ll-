from fastapi import FastAPI
from database import engine, Base
from modelos.user_model import User  # Importa tus modelos aquí
from handlers import router  # Importa tu router aquí
from modelos.citas_model import Cita
from modelos.doctores_model import Doctor
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

@app.on_event("startup")
async def startup():
    print("Starting up...")
    Base.metadata.create_all(bind=engine)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Ajusta esto a la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router) # Incluye tu router aquí   