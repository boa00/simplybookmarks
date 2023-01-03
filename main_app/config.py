from pydantic import BaseModel

class OpenIDConfig(BaseModel):

    oauth_endpoint: str = "https://accounts.google.com/o/oauth2/v2/auth?"
    token_endpoint: str = "https://oauth2.googleapis.com/token"
    response_type: str = "code"
    scope: str = "openid email profile"
    redirect_uri: str = "http://localhost:3000/google_openid"
    grant_type: str = "authorization_code"