from turtle import title
from typing import Optional
from pydantic import BaseModel 
from fastapi import FastAPI
from fastapi import Body, Query, Path

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
    name:Optional[str] = Query(
        None, min_length=1, 
        max_length=50,
        title='Person name',
        description='This is the person name, it`s between 1 and 50 characters'
        ),
    #Query Parameter obligatorio
    age: str =Query(
        ...,
        title= 'Person Age',
        description='The age of person it`s between 0 and 99, is a number and is required'
        )
):
    return{name:age}

#Validaciones Path Parameters
@app.get("/person/detail/{person_id}")
def showPerson(
    person_id: int = Path(
        ..., 
        gt=0,
        title= 'this is the person ID',
        description='It`s a number and required'
        )
):
    return{person_id: 'It exist'}