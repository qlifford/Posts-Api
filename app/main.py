from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

while True:
    try:
        conn =  psycopg2.connect(host='localhost', database='fastapiDb', user='postgres', password='Jahngily12', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Connection successful")
        break
    except Exception as error:
        print("Connection Failure")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"id": 1, "title": "post1 title", "content": "content of post1"}, {"id": 2, "title": "post2 title", "content": "content of post2"}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"data": "My home"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"details": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # print (type(id))
    post = find_post(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Post {id} does't not exist"
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"{id} was not found"}
    return {"post_details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Post {id} does't not exist"
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Post {id} does't not exist"
        )
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'post': post_dict}