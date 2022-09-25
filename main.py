
from email.policy import default
from enum import Enum
from importlib.resources import path
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, status
from fastapi import Body, Query, Path, Form

app = FastAPI()

class LoginOut(BaseModel):
    username: str = Field(...,min_length=1, max_length=20, example='jpardo107')
    message: str = Field(default='Login Succesfully!!')

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

class PersonModel(BaseModel):
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
#Validaciones de Modelo
class Person(PersonModel):
    password: str = Field(..., min_length=8, example = '12345678')

class  PersonOut(PersonModel):
    pass
    
#comando para correr la API
# uvicorn main:app --reload

#path Operations decorators
@app.get(
    path="/", 
    status_code=status.HTTP_200_OK
    )
#path operation functions
def home():
    return{'Hello':'World'}

#Request and Response Body

@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def createPerson(person:Person = Body(...)):
    return(person)

#Validaciones Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
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
@app.get(
    path="/person/detail/{person_id}"
    )
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

@app.put(
    path='/person/{person_id}'
    )
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

@app.post(
    path='/login',
    response_model =LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username = username)