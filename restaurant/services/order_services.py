from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from restaurant import database, models, schemas


class OrderService:
    @staticmethod
    def get_all_orders(db: Session = Depends(database.get_db)):  # fetch all orders
        orders = db.query(models.Orders).all()
        return orders

    @staticmethod
    def get_specific_order(order_id, db: Session = Depends(database.get_db)):
        order = db.query(models.Orders).get(order_id)
        # order = db.query(models.Orders).filter(models.Orders.order_id == order_id).first()(less efficient)
        if order is None:  # returns 404 response code if there is no such order_id
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'details': f"Order with the id {order_id} is not found"}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Order with the id {order_id} is not found')  # embedded function with FastAPI
        return order

    @staticmethod
    def create_order(request: schemas.OrderSchema, db: Session = Depends(database.get_db)):
        new_order = models.Orders(customer_id=1, dish=request.dish)
        db.add(new_order)  # add new record
        db.commit()  # commit changes
        db.refresh(new_order)  # refresh database
        return new_order

    @staticmethod
    def delete_order(order_id: int, db: Session = Depends(database.get_db)) -> dict:
        order = db.query(models.Orders).filter(models.Orders.order_id == order_id)  # ORM delete function
        if order.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Order with the id {order_id} is not found')
        order.delete(synchronize_session=False)
        db.commit()  # after deleting database record we should commit it
        return {'details': f'Order with the id {order_id} was deleted'}

    @staticmethod
    def update_order(request: schemas.OrderSchema, order_id: int, db: Session = Depends(database.get_db)):

        order = db.query(models.Orders).filter(models.Orders.order_id == order_id).first()

        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Order with the id {order_id} is not found')
        # order.update({models.Orders.customer_id: request.customer_id, models.Orders.dish: request.dish},
        #              synchronize_session=False)  # ORM update function
        order.customer_id = request.customer_id
        order.dish = request.dish
        db.commit()
        return {'details': f'Order with the id {order_id} has been updated'}
