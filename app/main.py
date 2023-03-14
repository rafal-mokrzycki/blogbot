from fastapi import FastAPI

# from app.api import audit
from app.api.models import (
    UserBase,
    UserIn,
    UserInDB,
    UserOut,
    get_user,
    save_user,
)

app = FastAPI()

# app.include_router(audit.router)


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = save_user(user_in)
    return user_saved


@app.get("/user/", response_model=UserOut)
async def show_user(user_out: UserOut):
    user_saved = get_user(user_out)
    return user_saved
