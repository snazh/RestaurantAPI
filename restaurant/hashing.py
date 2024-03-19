from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt(pwd: str) -> str:  # method for password hashing utilizing passlib
    hashed_pwd = pwd_context.hash(pwd)
    return hashed_pwd
