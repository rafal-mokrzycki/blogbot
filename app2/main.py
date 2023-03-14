# https://www.youtube.com/watch?v=GN6ICac3OXY
from typing import List
from uuid import UUID

from fastapi import FastAPI

from app.models import Gender, Role, User

app = FastAPI()
db: List[User] = [
    User(
        id=UUID("cc682793-2764-488c-88b3-ceda51d874e6"),
        first_name="Anna",
        last_name="Nowak",
        gender=Gender.female,
        roles=[Role.student],
    ),
    User(
        id=UUID("d155113b-2aed-4f6b-bfba-8bbb6ab59a31"),
        first_name="Jan",
        last_name="Kowalski",
        gender=Gender.male,
        roles=[Role.admin, Role.user],
    ),
]


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}
