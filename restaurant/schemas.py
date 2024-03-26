from pydantic import BaseModel
from typing import List


class UserBasicSchema(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True


class UserSchema(UserBasicSchema):
    password: str


class OrderSchema(BaseModel):
    customer_id: int
    dish: str

    class Config:
        from_attributes = True


class ShowUserSchema(UserBasicSchema):
    orders: List[OrderSchema] = []  # displaying list of customer's orders


class ShowOrderSchema(BaseModel):  # it is used to show specific info in JSON file
    customer: UserBasicSchema
    dish: str

    class Config:  # way to configure ORM behavior (Pydantic V2 and later)
        from_attributes = True


class LoginSchema(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
