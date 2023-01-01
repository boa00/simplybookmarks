import os

import jwt
from django.core.exceptions import ObjectDoesNotExist
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import authentication

from main_app.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) != 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != self.authentication_header_prefix.lower():
            return None

        return self._authenticate_credentials(token)

    def _authenticate_credentials(self, token):
        try:
            decoded_token = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=["HS256"])
        except ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except InvalidSignatureError:
            raise AuthenticationFailed("Signature verification failed")
        except DecodeError:
            raise AuthenticationFailed("Token could not be decoded")

        if decoded_token["token_type"] != "access":
            raise AuthenticationFailed(f"Access token was expected, got another type instead")

        try:
            user = User.objects.get(pk=decoded_token["user_id"])
        except ObjectDoesNotExist:
            raise AuthenticationFailed("User provided in the token does not exist")

        return (user, None)