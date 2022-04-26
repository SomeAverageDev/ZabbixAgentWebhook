"""
Goal: Implement basic HTTP authentication login/password logic
@authors:
    Gaël MONDON
"""
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.config import defaults

# authentication
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Validate username/password
    """
    correct_username = secrets.compare_digest(credentials.username, defaults['username'])
    correct_password = secrets.compare_digest(credentials.password, defaults['password'])

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return True
