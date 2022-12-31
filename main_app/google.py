import requests
import os 
import hashlib
import urllib.parse

import jwt


class OpenIDConnectHandler:

    # add constants to separate config file
    oauth_endpoint = "https://accounts.google.com/o/oauth2/v2/auth?"
    toeken_endpoint = "https://oauth2.googleapis.com/token"
    response_type = "code"
    scope = "openid email profile"
    redirect_uri = "http://127.0.0.1:1337/google_openid"
    grant_type = "authorization_code"

    def __init__(self) -> None:
        self.state = hashlib.sha256(os.urandom(1024)).hexdigest()
        self.nonce = hashlib.sha256(os.urandom(1024)).hexdigest()
        self.client_id = os.environ['GOOGLE_CLEINT_ID']
        self.client_secret = os.environ['GOOGLE_CLIENT_SECRET']

    def generate_openid_link(self) -> str:

        openid_params = {
            "client_id": self.client_id,
            "response_type": self.response_type,
            "scope": self.scope,
            "redirect_uri": self.redirect_uri,
            "state": self.state,
            "nonce": self.nonce,
        }

        url = self.oauth_endpoint + urllib.parse.urlencode(openid_params)
        return url

    def get_access_data(self, code: str) -> dict:
        request_params = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": self.grant_type,
        }

        response = requests.post(self.toeken_endpoint, params=request_params)
        response_data = response.json()
        return response_data
    
    def get_user_data(self, code: str):
        response_data = self.get_access_data(code=code)
        token_id = response_data["id_token"]
        all_user_data = jwt.decode(token_id, options={"verify_signature": False})
        user_data = {
            "email": all_user_data.get("email", None),
            "name": all_user_data.get("given_name", None),
        }
        return user_data

from rest_framework_simplejwt.tokens import RefreshToken
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
