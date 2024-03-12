from .database import Base
from sqlalchemy import Column, Integer, String


class Orders(Base):  # model for Orders table
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True, index=True)
    customer = Column(String)
    dish = Column(String)
