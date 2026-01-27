"""
Authentication: password hashing, JWT generation, login, registration.
"""

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

# Dependency: pip install passlib[bcrypt] python-jose

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET", "devsecret")
JWT_ALGORITHM = "HS256"
JWT_EXP_MINUTES = int(os.getenv("JWT_EXP_MINUTES", 60*24))

# PUBLIC_INTERFACE
def get_password_hash(password):
    """Return hash of a password."""
    return pwd_context.hash(password)

# PUBLIC_INTERFACE
def verify_password(plain_password, hashed_password):
    """Verify password."""
    return pwd_context.verify(plain_password, hashed_password)

# PUBLIC_INTERFACE
def create_access_token(data: dict, expires_delta=None):
    """Create JWT access token."""
    to_encode = data.copy()
    exp = datetime.utcnow() + (expires_delta or timedelta(minutes=JWT_EXP_MINUTES))
    to_encode.update({"exp": exp})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

# PUBLIC_INTERFACE
def decode_access_token(token: str):
    """Decode JWT access token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
