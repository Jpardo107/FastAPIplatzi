from typing import Optional
from pydantic import BaseModel 
from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

class Person(BaseModel):
    #Requeridos
    Nombre: str
    Apellido: str
    Edad: int
    #opcionales
    colorPelo: Optional[str] = None
    Casado: Optional[bool] = None

#comando para correr la API
# uvicorn main:app --reload

#path Operations decorators
@app.get("/")
#path operation functions
def home():
    return{'Hello':'World'}

#Request and Response Body

@app.post("/person/new")

def createPerson(person:Person = Body(...)):
    return(person)
