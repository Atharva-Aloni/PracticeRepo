from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from fastapi import status

class Post(BaseModel):
    id:int    
    name:str
    branch:str
def find_dict(id):
    for index,val in enumerate(l):
        if(val['id']==id):
            return val
app = FastAPI()
l = []

@app.get('/')
def root_function():
    return "What's Up gang"
@app.post('/create',status_code=status.HTTP_201_CREATED)
def post_creation(payload:Post):
    l.append(payload.dict())
    return "post created"

@app.get('/GetPost/{id}')
def find_post(id:int):
    d = find_dict(id)
    return d