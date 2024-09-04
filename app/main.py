from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app import models
from app.routes import auth, user, todo
from app.db import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(todo.router)