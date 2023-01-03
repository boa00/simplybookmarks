import requests
import os 
import hashlib
import urllib.parse
from typing import Dict

import jwt

from main_app.config import OpenIDConfig

class OpenIDConnectHandler:

    def __init__(self) -> None:
        self.state = hashlib.sha256(os.urandom(1024)).hexdigest()
        self.nonce = hashlib.sha256(os.urandom(1024)).hexdigest()
        self.client_id = os.environ['GOOGLE_CLEINT_ID']
        self.client_secret = os.environ['GOOGLE_CLIENT_SECRET']
        self.conf = OpenIDConfig()

    def generate_openid_link(self) -> str:

        openid_params = {
            "client_id": self.client_id,
            "response_type": self.conf.response_type,
            "scope": self.conf.scope,
            "redirect_uri": self.conf.redirect_uri,
            "state": self.state,
            "nonce": self.nonce,
        }

        url = self.conf.oauth_endpoint + urllib.parse.urlencode(openid_params)
        return url

    def get_access_data(self, code: str) -> dict:
        request_params = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.conf.redirect_uri,
            "grant_type": self.conf.grant_type,
        }

        response = requests.post(self.conf.token_endpoint, params=request_params)
        response_data = response.json()
        return response_data
    
    def get_user_data(self, code: str) -> Dict[str, str]:
        response_data = self.get_access_data(code=code)
        token_id = response_data["id_token"]
        all_user_data = jwt.decode(token_id, options={"verify_signature": False})
        user_data = {
            "email": all_user_data["email"],
        }
        return user_data

