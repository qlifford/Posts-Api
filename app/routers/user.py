from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import get_db


router  = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"User with id: {id} does't not exist")
    return user
