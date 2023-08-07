from fastapi import FastAPI
import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from router import posts, users, auth, votes

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "localhost:5500/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get('/')
def entry():
    return {"message": "Hello Ubuntu!"}
