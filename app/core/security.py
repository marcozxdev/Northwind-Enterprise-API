# jwt y hash de datos

# JWT
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError 
from app.core.config import settings






def create_acces_token(data: dict, exp_delta: timedelta | None):
    payload = data.copy()

    if exp_delta:
        expire = datetime.now(timezone.utc) + exp_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload.update({
        "exp": expire,
    })

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    



def decode_access_token(token: str):

    try:
        payload: dict = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        return payload

    except JWTError:
        return None



# hash
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"]
)



def hash_pwd(password: str):
    return pwd_context.hash(password)



def verify_pwd(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



