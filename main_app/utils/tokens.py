import os
from typing import Dict, Union
from datetime import datetime, timedelta

import jwt


def refresh_token_is_valid(token):
    decoded_token = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=["HS256"])

    if decoded_token["token_type"] != "access":
        raise ValueError("Provided token is not of the refresh type")

    now = int(datetime.now().strftime('%s'))
    if decoded_token["exp"] <= now:
        raise ValueError("Refresh token has expired")


    return decoded_token

def get_token(payload_data: Dict[str, Union[str, int]], token_type: str):
    iat = datetime.now()
    exp = iat + timedelta(minutes=10)
    payload_data.update({
        "token_type": token_type,
        "iat": int(iat.strftime('%s')),
        "exp": int(exp.strftime('%s')),
    })
    encoded_jwt = jwt.encode(payload_data, os.environ["SECRET_KEY"], algorithm="HS256")
    return encoded_jwt

def generate_tokens(payload_data: Dict[str, Union[str, int]]):
    access_token = get_token(payload_data=payload_data, token_type="access")
    refresh_token = get_token(payload_data=payload_data, token_type="refresh")
    tokens = {
        "access": access_token,
        "refresh": refresh_token,
    }
    return tokens


payload_data = {"email": "test@email.com", "id": 1}
tokens = generate_tokens(payload_data=payload_data)
access = tokens["access"]
refresh = tokens["refresh"]

print(token_is_valid(access))
