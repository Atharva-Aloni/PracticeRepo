from fastapi import FastAPI,Response,HTTPException,status
from fastapi import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

class PostValidation(BaseModel):
   id:int
   name: str
   branch: str
   age : int

try:
   conn = psycopg2.connect(host='localhost',database='atharva',user='postgres',password='root',port=5433,cursor_factory=RealDictCursor)
   cursor = conn.cursor()
   print("database is connected")
except Exception as error:
   print(error)   

my_post = [{'id':1,'name':'atharva','branch':'aiml','age':21},{'id':2,'name':'john doe','branch':'aiml','age':22}]
def find_dict(id):
   for i in my_post:
      if(i['id']==id):
         return i
      
def post_index(id):
   for index,val in enumerate(my_post):
      if(val['id']==id):
         return index
   return None
@app.get('/')
async def root():
   cursor.execute('''SELECT * FROM students ''')
   data = cursor.fetchall()
   print(data)
   return data

@app.post('/create',status_code=status.HTTP_201_CREATED)
async def create(post:PostValidation,reponse:Response):
   print(post)
   my_post.append(post.dict())
   p1 = post.dict()
   cursor.execute(''' INSERT INTO students VALUES(%s,%s,%s,%s) ''',(p1['id'],p1['name'],p1['branch'],p1['age']))
   conn.commit()
   return "This is creating post endpoint and validating the data is been received by payload"
@app.get('/post_count')
def post_num():
   return my_post


@app.get('/post/{id}')
def fetch_post_id(id:int,response:Response):
   d = find_dict(id)
   if not d:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"id - {id} not exist in database")
      #response.status_code = status.HTTP_404_NOT_FOUND
      #return {"message":f"id - {id} not exist in database"}
   return d
@app.delete('/PostDelete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def post_deletion(id:int):
   index = post_index(id)

   if index == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"provided id does not exist")

   my_post.pop(index)
   return Response(status_code=status.HTTP_204_NO_CONTENT)
@app.put('/PostUpdate/{id}')                                     # this is used for the updation operation in the fast api 
def post_updation(id:int,post:PostValidation):
   index = post_index(id)

   if index == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"value for {id} does not exist ")
   post_dict = post.dict()
   post_dict['id']=id
   my_post[index] = post_dict

   return {"data":post_dict}