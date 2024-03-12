from pydantic import BaseModel


class OrderSchema(BaseModel):
    customer: str
    dish: str


class ShowOrderSchema(BaseModel):  # it is used to show specific info in JSON file
    customer: str
    dish: str

    class Config:  # way to configure ORM behavior (Pydantic V2 and later)
        from_attributes = True
