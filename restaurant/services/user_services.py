from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from restaurant import database, models, schemas, hashing


class UserServices:
    @staticmethod
    def get_all_users(db: Session = Depends(database.get_db)):
        """Fetch all users."""
        users = db.query(models.Users).all()

        return users

    @staticmethod
    def get_specific_user(user_id: int, db: Session = Depends(database.get_db)):
        """Fetch a specific user by user_id."""
        user = db.query(models.Users).get(user_id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'User with the id {user_id} is not found')
        return user

    @staticmethod
    def create_user(request: schemas.UserSchema, db: Session = Depends(database.get_db)):
        """Create a new user."""
        new_user = models.Users(username=request.username, email=request.email,
                                password=hashing.encrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
