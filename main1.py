from fastapi import FastAPI
from fastapi import requests,responses,HTTPException,status
from fastapi import Response
from fastapi import Body
from pydantic import BaseModel
class validate(BaseModel):
    name:str
    age:int

def find_index(id:int):
    for index,item in enumerate(li):
        if(item['id']==id):
            return index
    return None    

app = FastAPI()
li = [{"id":1,'name':"atharva","age":21},{"id":2,"name":"omkar","age":21}]
def find_dict(id:int):
    for index,item in enumerate(li):
        if item['id']==id:
            return item
@app.get('/')
def root_function():
    return "this is root function and I am implementing this for my practice purpose kindly consider"
@app.post('/create',status_code=status.HTTP_201_CREATED)
def create(val:validate):
    v1 = val.dict()
    li.append(v1)
    print(v1)
    return {"message":"Post Created"}
@app.get('/ListVal')
def print_list_val():
    return li
@app.get('/PostID/{id}')
def fun(id:int):
    d = find_dict(id)
    print(d)
    return d
@app.delete('/DeletePost/{id}')
def deletion(id:int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No tuple with {id} exist in the database ")
    li.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)    
@app.put('/PostUpdate/{id}')
def post_update(id:int,new_post:validate):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"tuple for {id} does not exist in the database ")
    p = new_post.dict()
    li[index]['name'] = p['name']
    li[index]['age'] = p['age']
    return f"post is updated successfully check the updation by hitting /ListVal"
    