from sqlalchemy.orm import relationship

from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Orders(Base):  # model for Orders table
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('users.user_id'))
    customer = relationship("Users", back_populates="orders")
    dish = Column(String)
    # dish_id = Column(Integer, ForeignKey('dishes.dish_id'))  # Foreign key
    # dishes = relationship("User", back_populates="orders")  # Connecting with ORM layer


# class Dishes(Base):
#     __tablename__ = 'dishes'
#     dish_id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     category_id = Column(Integer, ForeignKey('categories.category_id'))
#     category = relationship('DishCategories', back_populates="dishes")
#     orders = relationship("Orders", back_populates="dishes")
#
#
# class DishCategories(Base):
#     __tablename__ = 'categories'
#     category_id = Column(Integer)
#     category = Column(String)
#     dishes = relationship('Dishes', back_populates="category")


class Users(Base):  # model for Users table
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    orders = relationship("Orders", back_populates="customer")
