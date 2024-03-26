from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def encrypt(pwd: str) -> str:  # method for password hashing utilizing passlib
        hashed_pwd = pwd_context.hash(pwd)
        return hashed_pwd

    @staticmethod
    def verify(entered_pwd, hashed_pwd):  # method for password verifying utilizing passlib
        return pwd_context.verify(entered_pwd, hashed_pwd)
