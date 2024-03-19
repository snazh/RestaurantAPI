from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from restaurant.services.user_services import UserServices
from restaurant import database, schemas

router = APIRouter(
    prefix="/users",
    tags=['Users'],  # tags are used to categorize endpoints

    responses={200: {"description": "Success"}})


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.UserSchema, db: Session = Depends(database.get_db)):
    return UserServices.create_user(request, db)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.UserBasicSchema])
async def get_all_users(db: Session = Depends(database.get_db)):
    return UserServices.get_all_users(db)


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUserSchema)
async def get_specific_user(user_id: int, db: Session = Depends(database.get_db)):
    return UserServices.get_specific_user(user_id, db)
