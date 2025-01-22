from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

security = HTTPBearer()

TOKEN = os.getenv("BEARER_TOKEN", "SECRET_BEARER_TOKEN")

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    if credentials.credentials != TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    return True
