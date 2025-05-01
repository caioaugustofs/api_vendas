from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=5,
        max_length=20,
        description='Nome de usuário deve ter entre 5 e 20 caracteres',
    )
    email: EmailStr = Field(
        ...,
        description='Email deve ser um email válido',
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
        description='Senha deve ter entre 8 e 20 caracteres',
    )


class userPublic(BaseModel):
    id: int
    username: str
    email: str


class UserList(BaseModel):
    users: list[userPublic]


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
