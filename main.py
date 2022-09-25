
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

class ColorPelo(Enum):
    white ='White'
    brown = 'Brown'
    black = 'Black'
    blonde = 'Blonde'
    red = 'Red'


class Location(BaseModel):
    city: str
    state: str
    country: str
#Validaciones de Modelo
class Person(BaseModel):
    #Requeridos
    Nombre: str = Field(
        ...,
        min_length=1,
        max_length=30,
        example='Daniel'
        )
    Apellido: str = Field(
        ...,
        min_length=1,
        max_length=30,
        example='Maldonado'
        )
    Edad: int =Field(
        ...,
        gt=0,
        le=115,
        example=15
        )
    #opcionales
    colorPelo: Optional[ColorPelo] = Field(default = None, example='Brown')
    Casado: Optional[bool] = Field(default=None, example='true')
    password: str = Field(..., min_length=8, example = '12345678')

class  PersonOut(BaseModel):
     #Requeridos
    Nombre: str = Field(
        ...,
        min_length=1,
        max_length=30,
        example='Daniel'
        )
    Apellido: str = Field(
        ...,
        min_length=1,
        max_length=30,
        example='Maldonado'
        )
    Edad: int =Field(
        ...,
        gt=0,
        le=115,
        example=15
        )
    #opcionales
    colorPelo: Optional[ColorPelo] = Field(default = None, example='Brown')
    Casado: Optional[bool] = Field(default=None, example='true')
 
    #Dentro de la misma clase
    # class Config:
    #     schema_extra = {
    #         "example" :{
    #             'Nombre': 'Jaime',
    #             'Apellido': 'Pardo',
    #             'Edad': 32,
    #             'colorPelo': 'Blonde',
    #             'Casado': 'false'
    #         }
    #     }

#comando para correr la API
# uvicorn main:app --reload

#path Operations decorators
@app.get("/")
#path operation functions
def home():
    return{'Hello':'World'}

#Request and Response Body

@app.post("/person/new", response_model=PersonOut)
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
        description='This is the person name, it`s between 1 and 50 characters',
        example='Doris'
        ),
    #Query Parameter obligatorio
    age: str =Query(
        ...,
        title= 'Person Age',
        description='The age of person it`s between 0 and 99, is a number and is required',
        example=42
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
        description='It`s a number and required',
        example=3
        )
):
    return{person_id: 'It exist'}

#Validacion de Request Body

@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title='Person ID',
        description='This is a person id, it`s a number and required',
        gt=0,
        example=6
        ),
        person: Person = Body(...),
        #Location: Location = Body(...)
):
    # result = person.dict()
    # result.update(Location.dict())
    return person