import requests
import os 
import hashlib
import json 
import urllib.parse

import jwt


class OpenIDConnectHandler:

    oauth_endpoint = "https://accounts.google.com/o/oauth2/v2/auth?"
    toeken_endpoint = "https://oauth2.googleapis.com/token"
    response_type = "code"
    scope = "openid email profile"
    redirect_uri = "http://127.0.0.1:1337/google_openid"

    def __init__(self) -> None:
        self.state = hashlib.sha256(os.urandom(1024)).hexdigest()
        self.nonce = hashlib.sha256(os.urandom(1024)).hexdigest()

    # move two methods below to the env variables
    def _get_client_id(self) -> str:
        secrets_json = open('main_app/openid_secrets.json')
        client_id = json.load(secrets_json)["web"]["client_id"]
        secrets_json.close()
        return client_id

    def _get_client_secfet(self) -> str:
        secrets_json = open('main_app/openid_secrets.json')
        client_id = json.load(secrets_json)["web"]["client_secret"]
        secrets_json.close()
        return client_id

    def generate_openid_link(self) -> str:
        client_id = self._get_client_id()

        openid_params = {
            "client_id": client_id,
            "response_type": self.response_type,
            "scope": self.scope,
            "redirect_uri": self.redirect_uri,
            "state": self.state,
            "nonce": self.nonce,
        }

        url = self.oauth_endpoint + urllib.parse.urlencode(openid_params)
        return url

    def get_access_data(self, code: str) -> dict:
        client_id = self._get_client_id()
        client_secret = self._get_client_secfet()
        request_params = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }

        response = requests.post(self.toeken_endpoint, params=request_params)
        response_data = response.json()
        return response_data
    
    def get_user_data(self, code: str):
        response_data = self.get_access_data(code=code)
        token_id = response_data["id_token"]
        all_user_data = jwt.decode(token_id, options={"verify_signature": False})
        user_data = {
            "email": all_user_data["email"],
            "name": all_user_data["given_name"]
        }
        return user_data

def generate_openid_link():
    secrets_json = open('main_app/openid_secrets.json')
    secrets = json.load(secrets_json)["web"]
    secrets_json.close()

    openid_params = {
        "client_id": secrets["client_id"],
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": "http://127.0.0.1:1337/google_openid",
        "state": hashlib.sha256(os.urandom(1024)).hexdigest(),
        "nonce": hashlib.sha256(os.urandom(1024)).hexdigest(),
        #"hint": "olegblanutsa@gmail.com",
    }

    oauth_endpoint = "https://accounts.google.com/o/oauth2/v2/auth?"
    url = oauth_endpoint + urllib.parse.urlencode(openid_params)
    return url

handler = OpenIDConnectHandler()
print(handler.generate_openid_link())
