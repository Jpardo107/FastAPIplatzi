#Python
from enum import Enum
from typing import Optional
#Pydantic
from pydantic import BaseModel 
from pydantic import Field
from pydantic import EmailStr
#FastAPI
from fastapi import FastAPI  
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

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
    status_code=status.HTTP_200_OK,
    tags=['Home'],
    summary='App home page'
    )
#path operation functions
def home():
    """
    Home Page

    This path operation display de message Hello World in a dictionary format
    
    Parameters:
    - No parameters

    Returns a dictionary {'Hello':'World'}
    """
    return{'Hello':'World'}

#Request and Response Body

@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=['Persons'],
    summary='Create person in the app'
    )
def createPerson(person:Person = Body(...)):
    """
    Create Person

    This path operation create a person in the app and save the information in the database
    
    Parameters:
    - Request body parameter:
        - **person: Person** -> A person model with firstname, age, hair color and marital status

    Returns a person model with firstname, age, hair color and marital status
    """
    return(person)

#Validaciones Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary='Show person detail saved in the app'
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
    """
    Show person detail

    This path operation show person details saved in the app
    
    Parameters:
    - Response body parameter:
        - **person: Person** -> A person model with firstname and age

    Returns a person model with firstname and age in a dictionary format
    """
    return{name:age}

#Validaciones Path Parameters

persons=[1,2,3,4,5]

@app.get(
    path="/person/detail/{person_id}",
    tags=['Persons'],
    summary='Show if a person exist or not in the app'
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
    """
    Show if person exist

    This path operation show if a person exist in the app with the id provided
    
    Parameters:
    - request body parameter:
        - **person_id: int** -> person id provided and will be compared with de saved id in the app

    Returns a message 'exist' or 'not exist' as appropriate
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='This person doesn`t exist!'
        )
    return{person_id: 'It exist'}

#Validacion de Request Body

@app.put(
    path='/person/{person_id}',
    tags=['Persons'],
    summary='Update person attributes with the id provided'
    )
def update_person(
    person_id: int = Path(
        ...,
        title='Person ID',
        description='This is a person id, it`s a number and required',
        gt=0,
        example=6,
        
        ),
        person: Person = Body(...),
        #Location: Location = Body(...)
):
    # result = person.dict()
    # result.update(Location.dict())

    """
    Update a person attributes according to the id provided

    This path operation update the selected person attributes that matched with de id provided
    
    Parameters:
    - request body parameter:
        - **person_id: int** -> person id provided and will be compared with de saved id in the app
        - **selected parameter** -> selected parameter and update

    Returns a person whit the updates made
    """

    return person
#Forms
@app.post(
    path='/login',
    response_model =LoginOut,
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary='Login user from a form'
)
def login(username: str = Form(...), password: str = Form(...)):
    """
    login a user

    This path operation login a user with a username and password
    
    Parameters:
    - request body parameter:
        - **username: LoginOut** -> username is a string from a form in the frontend
        - **password: str** -> password is a string from a form in the frontend

    Returns a username
    """
    return LoginOut(username = username)
#Cookies and Headers Parameters

@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=['Forms'],
    summary='Contact from a form in the frontend'
)
def contact(
    firstname: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    lastname: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20,
        max_length=255
    ),
    user_agent: Optional[str] = Header(default= None),
    ads: Optional[str] = Cookie(default= None)
):
    """
    form contact

    This path operation capture a contact request 
    
    Parameters:
    - request body parameter:
        - **username: str** -> username is a string from a form in the frontend
        - **password: str** -> password is a string from a form in the frontend

    Returns a username
    """
    return user_agent

#Files
@app.post(
    path='/post-image',
    tags=['Files']
    )
def post_image(
    image: UploadFile = File(...)
):
    return{
        'Filename': image.filename,
        'format': image.content_type,
        'size': round(len(image.file.read())/1024, ndigits=2)
    }