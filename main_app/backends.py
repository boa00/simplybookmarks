import jwt 
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User

class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = "Token"

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix
        print(auth_header)
        if not auth_header or len(auth_header) != 2:
            return None

        prefix, token = auth_header[0].decode('utf-8'), auth_header[1].decode('utf-8')
        if prefix.lower() != auth_header_prefix.lower():
            return None 
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        print(token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except Exception:
            error_msg = "Token could not be parsed"
            raise exceptions.AuthenticationFailed(error_msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            error_msg = "User does not exist"
            raise exceptions.AuthenticationFailed(error_msg)

        if not user.is_active:
            error_msg = "User has been deactivated"
            raise exceptions.AuthenticationFailed(error_msg)

        return (user, token)