from typing import Optional
from pydantic import BaseModel 
from fastapi import FastAPI
from fastapi import Body, Query

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

#Validaciones Query Parameters

@app.get("/person/detail")
def showPerson(
    #Query Parameter obligatorio
    name:Optional[str] = Query(None, min_length=1, max_length=50),
    #Query Parameter obligatorio
    age: str =Query(...)
):
    return{name:age}