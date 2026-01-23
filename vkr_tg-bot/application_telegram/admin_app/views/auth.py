from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta

from admin_app.schemas.auth import *
from admin_app.services.admins import authenticate_admin, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


auth_router = APIRouter()


@auth_router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_admin(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "isa": user["is_superadmin"]}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
