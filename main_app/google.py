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
        token_id = response_data["token_id"]
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

#print(generate_openid_link())

hash_val = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjhjMjdkYjRkMTNmNTRlNjU3ZDI2NWI0NTExMDA4MGI0ODhlYjQzOGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzOTY0MzMzMTA3MjEtZTI2YW11MmMwdGo5cWl1NGppaXY5dWFvM2M1a2w1cmguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIzOTY0MzMzMTA3MjEtZTI2YW11MmMwdGo5cWl1NGppaXY5dWFvM2M1a2w1cmguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDczNjk0ODk1Nzg5MzAwOTI1MjMiLCJlbWFpbCI6Im9sZWdibGFudXRzYUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6IkRVeXJma1RhMjBiajN4Y19nX3pOQUEiLCJub25jZSI6IjRkZDU1ODBjNjFiZjY4MTNiNDYzZjY3MjI3OTNiMjliZjcxNGNkN2I4YzJlNWQzMDE4MmQ2ZDkzMWI2MmRkODEiLCJuYW1lIjoiT2xlZyBCbGFudXRzYSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BRWRGVHA1ZmRfdGtSTnlISXBMR1pGNkRraW9rX3ZhS1hleXlFZ3lWbDBLNWRnPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6Ik9sZWciLCJmYW1pbHlfbmFtZSI6IkJsYW51dHNhIiwibG9jYWxlIjoiZW4tR0IiLCJpYXQiOjE2NzEyMDk1OTAsImV4cCI6MTY3MTIxMzE5MH0.U2tBZBWZdrQaNxEWoI8gi2f5ICofNcUf5bWjDwFO5jlfPNW47DltpT33FPZTKnAjtGDvC7R4-_v9dGPi24Mxqu1xCREwdt4K4-ttyNpZGEDdpVrSpz8UeHP2HzED03eOnjGHW5iz7sZ7VU0F4TQlrnr9G8QadJa84qeU8n2fUt2hvi3WQ-Y8aQCXonvRkC5DHx5VjbZETmP2CMxKxRciKqSb3hGmt3DdMIwZmSd2elF6-xgYaD1ZmUJ-wzQ8JOUJvWwvw6X6hXkKKYD3ilLblLhQ6BMahKZ4Vvcq_E2ccsY9SXJxhYpQ7UaA2R2HHQXfDFkrSrhx5nlEXMzMa8Yq6w"

import jwt
secrets_json = open('main_app/openid_secrets.json')
secret_key = json.load(secrets_json)["web"]["client_secret"]
secrets_json.close()
payload = jwt.decode(hash_val, options={"verify_signature": False})
print(payload)

# personal_info_encoded = hash_val.split('.')[1]
# b64string = personal_info_encoded 
# padded = b64string + '=' * (4 - len(b64string) % 4) 
# info = base64.urlsafe_b64decode(padded)
# print(type(info))
