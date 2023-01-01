import os
from typing import Dict, Union
from datetime import datetime, timedelta

import jwt
from django.core.exceptions import ObjectDoesNotExist
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from rest_framework.serializers import ValidationError 

from main_app.models import User

def refresh_token_is_valid(token) -> bool:
    try:
        decoded_token = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=["HS256"])
    except ExpiredSignatureError:
        raise ValidationError("Refresh token has expired")
    except InvalidSignatureError:
        raise ValidationError("Signature verification failed")

    if decoded_token["token_type"] != "refresh":
        raise ValidationError(f"Refresh token was expected, got another type instead")

    try:
        user = User.objects.get(pk=decoded_token["user_id"])
    except ObjectDoesNotExist:
        raise ValidationError(f"User provided in the token does not exist")

    if user.email != decoded_token["email"]:
        raise ValidationError(f"User with email provided in the token does not exist")
    
    return True


def get_token(payload_data: Dict[str, Union[str, int]], token_type: str, exp_time: int) -> str:
    iat = datetime.now()
    exp = iat + timedelta(minutes=exp_time)
    payload_data.update({
        "token_type": token_type,
        "iat": int(iat.strftime('%s')),
        "exp": int(exp.strftime('%s')),
    })
    encoded_jwt = jwt.encode(payload_data, os.environ["SECRET_KEY"], algorithm="HS256")
    return encoded_jwt

def generate_tokens(payload_data: Dict[str, Union[str, int]]) -> Dict[str, str]:
    access_token = get_token(payload_data=payload_data, token_type="access", exp_time=10)
    refresh_token = get_token(payload_data=payload_data, token_type="refresh", exp_time=60*24*30)
    tokens = {
        "access": access_token,
        "refresh": refresh_token,
    }
    return tokens
