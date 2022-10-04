# tokens.py
import jwt
import datetime
from decouple import config

def generate_token(payload, type):
    if type == "access":
        # 2시간
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    elif type == "refresh":
        # 2주
        exp = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
    else:
        raise Exception("Invalid tokenType")
    
    payload['exp'] = exp
    payload['iat'] = datetime.datetime.utcnow()
    encoded = jwt.encode(payload, config("JWT_SECRET_KEY"), algorithm=config("JWT_ALGORITHM"))

    return encoded