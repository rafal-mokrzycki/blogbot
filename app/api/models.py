import logging

from pydantic import BaseModel, EmailStr
from werkzeug.security import generate_password_hash

log = logging.getLogger(__name__)


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def password_hasher(raw_password: str, method="pbkdf2:sha256", salt_length=8):
    return generate_password_hash(
        raw_password, method=method, salt_length=salt_length
    )


def save_user(user_in: UserIn):
    hashed_password = password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    log.info("User saved.")
    return user_in_db


def get_user(user_out: UserOut):
    user_in_db = UserInDB(**user_out.dict())
    return user_in_db
