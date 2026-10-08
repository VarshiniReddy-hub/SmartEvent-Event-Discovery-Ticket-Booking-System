from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from security import (
    bearer_scheme,
    get_current_user_id,
    get_current_user_role
)


# =========================
# CURRENT USER
# =========================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    )
):
    user_id = get_current_user_id(credentials)
    role = get_current_user_role(credentials)

    return {
        "user_id": user_id,
        "role": role
    }


# =========================
# ORGANIZER ONLY
# =========================

def require_organizer(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "ORGANIZER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer access required"
        )

    return current_user


# =========================
# ADMIN ONLY
# =========================

def require_admin(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user


# =========================
# USER ONLY
# =========================

def require_user(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "USER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User access required"
        )

    return current_user