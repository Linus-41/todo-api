from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.database import db
from app.routes import auth, user, todo, category
from app.database.db import engine


app = FastAPI()

db.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(todo.router)
app.include_router(category.router)
