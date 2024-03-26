from typing import List
from restaurant.services.order_services import OrderService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from restaurant import database, schemas, oauth2

router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)


# get all orders
@router.get('/', response_model=List[schemas.ShowOrderSchema])
async def get_all_orders(current_user: schemas.UserSchema = Depends(oauth2.get_current_user),
                         db: Session = Depends(database.get_db)):
    return OrderService.get_all_orders(db)


# create order
@router.post('/', status_code=status.HTTP_201_CREATED)  # 201 - is 'created' response code
async def post_order(request: schemas.OrderSchema, current_user: schemas.UserSchema = Depends(oauth2.get_current_user),
                     db: Session = Depends(database.get_db)):  # create order
    return OrderService.create_order(request, db)


# get order
@router.get('/{order_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowOrderSchema)
async def get_specific_order(order_id: int, current_user: schemas.UserSchema = Depends(oauth2.get_current_user),
                             db: Session = Depends(database.get_db)):
    return OrderService.get_specific_order(order_id, db)


# delete order
@router.delete('/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, current_user: schemas.UserSchema = Depends(oauth2.get_current_user),
                       db: Session = Depends(database.get_db)):
    return OrderService.delete_order(order_id, db)


# update order
@router.put('/{order_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_order(order_id: int, request: schemas.OrderSchema,
                       current_user: schemas.UserSchema = Depends(oauth2.get_current_user),
                       db: Session = Depends(database.get_db)):
    return OrderService.update_order(request, order_id, db)
