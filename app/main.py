from fastapi import FastAPI, HTTPException, status , Depends
from fastapi.middleware.cors import CORSMiddleware
from . import model
from .database import engine, get_db
from sqlalchemy.orm import Session
from .enumProvider import Genre
from . import schemas
from . import utils
from .Routers import book, borrower , auth,transaction, upvote


#model.Base.metadata.create_all(bind = engine)
#code that asked SQLAlchemy to run the sql query to create the Tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your React app's origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

my_issues = [
    {"title": "To Kill a Mockingbird", "genre": "Fiction","available_issues": 5},
    {"title": "1984", "genre": "Dystopian", "id": 456},
    {"title": "Pride and Prejudice", "genre": "Romance", "id": 789},
    {"title": "The Great Gatsby", "genre": "Classic", "id": 321},
    {"title": "The Lord of the Rings", "genre": "Fantasy", "id": 654},
    {"title": "Harry Potter and the Philosopher's Stone", "genre": "Fantasy", "id": 987},
    {"title": "The Catcher in the Rye", "genre": "Coming-of-Age", "id": 234},
    {"title": "The Hobbit", "genre": "Fantasy", "id": 567},
    {"title": "Moby-Dick", "genre": "Adventure", "id": 890},
    {"title": "To the Lighthouse", "genre": "Modernist", "id": 432}
]

@app.get("/")
async def root():
    return {"status":"success"}

app.include_router(book.router)

app.include_router(borrower.router)

app.include_router(auth.router)

app.include_router(transaction.router)

app.include_router(upvote.router)

