from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from random import randrange
from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from . database import engine, get_db
from . routers import post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

@app.get("/", status_code=status.HTTP_202_ACCEPTED)
def root():
    return "Welcome to the home page"
