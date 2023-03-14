from pathlib import Path
from typing import Any, Optional

from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    Form,
    HTTPException,
    Query,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.models import (
    UserBase,
    UserIn,
    UserInDB,
    UserOut,
    get_user,
    save_user,
)

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_router = APIRouter()

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_PATH / "static")),
    name="json",
)

templates = Jinja2Templates(
    directory=r"C:\Users\rafal\Documents\python\blogbot\app\templates"
)


@app.get("/", response_class=HTMLResponse)
async def data(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": form_data.username + "token"}


@app.post("/sth")
async def index(token: str = Depends(oauth2_scheme)):
    return {"the_token": token}


@app.post("/user", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = save_user(user_in)
    return user_saved


@app.get("/user", response_model=UserOut)
async def show_user(user_out: UserOut):
    user_saved = get_user(user_out)
    return user_saved
