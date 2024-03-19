from fastapi import FastAPI
from database import engine, Base
from modelos.user_model import User  # Importa tus modelos aquí
from handlers import router  # Importa tu router aquí


app = FastAPI()

@app.on_event("startup")
async def startup():
    # Crea las tablas
    Base.metadata.create_all(bind=engine)

app.include_router(router)  # Incluye tu router aquí    