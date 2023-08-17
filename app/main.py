from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from . database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/", status_code=status.HTTP_202_ACCEPTED)
def root():
    return "Welcome to the home page"


@app.get("/posts", response_model=List[schemas.Post])
def get_posts( db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return post


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post {id} does't not exist")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Post {id} does't not exist"
        )
    deleted_post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"Post {id} does't not exist")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()