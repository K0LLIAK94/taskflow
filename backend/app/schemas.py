from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LabelOut(BaseModel):
    id: int
    name: str
    color: str
    model_config = ConfigDict(from_attributes=True)


class CardCreate(BaseModel):
    title: str
    description: str = ""


class CardOut(BaseModel):
    id: int
    title: str
    description: str
    position: float
    column_id: int
    labels: List[LabelOut] = []
    model_config = ConfigDict(from_attributes=True)


class CardMove(BaseModel):
    column_id: int
    position: float


class ColumnCreate(BaseModel):
    title: str


class ColumnOut(BaseModel):
    id: int
    title: str
    position: float
    cards: List[CardOut] = []
    model_config = ConfigDict(from_attributes=True)


class BoardCreate(BaseModel):
    title: str


class BoardOut(BaseModel):
    id: int
    title: str
    columns: List[ColumnOut] = []
    model_config = ConfigDict(from_attributes=True)
