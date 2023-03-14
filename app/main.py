import datetime as dt
from pathlib import Path
from typing import Dict, List, Optional

import console
from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import (
    OAuth2,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

from app.api.models import UserBase, get_user
from app.api.settings import Settings

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "app/templates"))
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_router = APIRouter()

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_PATH / "static")),
    name="json",
)

templates = Jinja2Templates(directory="app/templates")
settings = Settings()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    try:
        user = get_current_user_from_cookie(request)
    except:
        user = None
    context = {
        "user": user,
        "request": request,
    }
    return templates.TemplateResponse("index.html", context)


@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("login.html", context)


@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = RedirectResponse("/", status.HTTP_302_FOUND)
            login_for_access_token(response=response, form_data=form)
            form.__dict__.update(msg="Login Successful!")
            console.log("[green]Login successful!!!!")
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)


@app.get("/private", response_class=HTMLResponse)
def private(request: Request, user: UserBase):
    context = {"user": user, "request": request}
    return templates.TemplateResponse("private.html", context)


@app.post("token")
def login_for_access_token(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, str]:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"username": user.username})

    # Set an HttpOnly cookie in the response. `httponly=True` prevents
    # JavaScript from reading the cookie.
    response.set_cookie(
        key=settings.COOKIE_NAME, value=f"Bearer {access_token}", httponly=True
    )
    return {settings.COOKIE_NAME: access_token, "token_type": "bearer"}


class OAuth2PasswordBearer(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": tokenUrl, "scopes": scopes}
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False


def authenticate_user(username: str, plain_password: str) -> UserBase:
    user = get_user(username)
    if not user:
        return False
    if not crypto.verify(plain_password, user.hashed_password):
        return False
    return user


def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> UserBase:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    token = token.removeprefix("Bearer").strip()
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception

    user = get_user(username)
    return user


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
) -> UserBase:
    """
    Get the current user from the cookies in a request.

    Use this function when you want to lock down a route so that only
    authenticated users can see access the route.
    """
    user = decode_token(token)
    return user


def get_current_user_from_cookie(request: Request) -> UserBase:
    """
    Get the current user from the cookies in a request.

    Use this function from inside other routes to get the current user. Good
    for views that should work for both logged in, and not logged in users.
    """
    token = request.cookies.get(settings.COOKIE_NAME)
    user = decode_token(token)
    return user


# @app.get("/", response_class=HTMLResponse)
# async def data(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# @app.post("/token")
# async def token(form_data: OAuth2PasswordRequestForm = Depends()):
#     return {"access_token": form_data.username + "token"}


# @app.post("/sth")
# async def index(token: str = Depends(oauth2_scheme)):
#     return {"the_token": token}


# @app.post("/user", response_model=UserBaseOut)
# async def create_user(user_in: UserBaseIn):
#     user_saved = save_user(user_in)
#     return user_saved


# @app.get("/user", response_model=UserBaseOut)
# async def show_user(user_out: UserBaseOut):
#     user_saved = get_user(user_out)
#     return user_saved
