import os
import jwt
import _credentials
import logging
# importing necessary functions from dotenv library
from dotenv import load_dotenv
# loading variables from .env file
load_dotenv()

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.WARNING,
)

ISSUER = os.environ.get("TOKEN_ISSUER")
AUDIENCE = os.environ.get("TOKEN_AUDIENCE")

if ISSUER is None:
    logging.warning("ISSUER is none, setting to Local")
    ISSUER = "Local"

if AUDIENCE is None:
    logging.warning("AUDIENCE is none, setting to locally")
    AUDIENCE = "locally"

with open("/run/secrets/private_key", "rb") as f:
    PRIVATE_KEY = f.read()

with open("/run/secrets/public_key", "rb") as f:
    PUBLIC_KEY = f.read()


# Create token for auth
def create_jwt(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "iss": ISSUER,
        "aud": AUDIENCE,
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

# Verify token for auth
def verify_jwt(token: str) -> dict:
    return jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)

def get_username(token: str) -> str:
    decoded_token = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)
    return decoded_token['sub']
