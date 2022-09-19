from fastapi import FastAPI

app = FastAPI()

#comando para correr la API
# uvicorn main:app --reload

#path Operations decorators
@app.get("/")
#path operation functions
def home():
    return{'Hello':'World'}