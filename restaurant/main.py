from typing import List

from fastapi import FastAPI, Depends, status, HTTPException
from .schemas import OrderSchema, ShowOrderSchema
from .models import *
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI(port=8080)  # FastAPI app initialization

Base.metadata.create_all(engine)  # migrating all models


def get_db():  # method for db connection
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/restaurant', status_code=status.HTTP_201_CREATED)  # 201 - is 'created' response code
async def post_order(request: OrderSchema, db: Session = Depends(get_db)):  # create order
    new_order = Orders(customer=request.customer, dish=request.dish)
    db.add(new_order)  # add new record
    db.commit()  # commit changes
    db.refresh(new_order)  # refresh database
    return new_order


@app.get('/restaurant', response_model=List[ShowOrderSchema])
async def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Orders).all()  # fetch all data
    return orders


# get order_id method
@app.get('/restaurant/{order_id}', status_code=status.HTTP_200_OK, response_model=ShowOrderSchema)
async def get_specific_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Orders).get(order_id)
    # order = db.query(models.Orders).filter(models.Orders.order_id == order_id).first()(less efficient)
    if order is None:  # returns 404 response code if there is no such order_id
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f'Order with the id {order_id} is not found'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Order with the id {order_id} is not found')  # embedded function with FastAPI
    return order


# delete order
@app.delete('/restaurant/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Orders).filter(Orders.order_id == order_id)  # ORM delete function
    if order.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Order with the id {order_id} is not found')
    order.delete(synchronize_session=False)
    db.commit()  # after deleting database record we should commit it
    return {'details': f'Order with the id {order_id} was deleted'}


@app.put('/restaurant/{order_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_order(order_id: int, request: OrderSchema, db: Session = Depends(get_db)):
    order = db.query(Orders).filter(Orders.order_id == order_id)

    if order.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Order with the id {order_id} is not found')
    order.update({Orders.customer: request.customer, Orders.dish: request.dish},
                 synchronize_session=False)  # ORM update function
    db.commit()
    return {'details': f'Order with the id {order_id} has been updated'}
