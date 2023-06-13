from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")





def bcrypted(password: str)->str:
        return pwd_cxt.hash(password)

def verify_password(normal: str, hashed: str)->bool:
        return pwd_cxt.verify(normal, hashed)

