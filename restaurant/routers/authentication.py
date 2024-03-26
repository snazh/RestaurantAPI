from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from restaurant.hashing import Hash

from restaurant import schemas, database, models, JWTtoken

router = APIRouter(

    tags=['authentication']
)


@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == request.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid credentials')
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid password')

    # generate a JWT token and return

    access_token = JWTtoken.create_access_token(data={"sub": user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
