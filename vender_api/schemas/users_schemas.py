from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class userPublic(BaseModel):
    id: int
    username: str
    email: str


class UserLisr(BaseModel):
    User: list[userPublic]


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    cpf: Optional[str] = None
    birth_date: Optional[str] = None
    cargo: Optional[str] = None


class UserPasswordUpdate(BaseModel):
    password: str


class UserIsActiveUpdate(BaseModel):
    is_active: bool = False


class UserIsSuperuserUpdate(BaseModel):
    is_superuser: bool = False


class UserIsVerifiedUpdate(BaseModel):
    is_verified: bool = False
