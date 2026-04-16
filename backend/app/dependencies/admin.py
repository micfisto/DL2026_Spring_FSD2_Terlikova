from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from ..db import get_db
from ..utils.security.jwt import verify_token
from ..models.admin_user import AdminUser


def get_current_admin(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    token = authorization.split(" ")[1]
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    admin = db.query(AdminUser).filter(
        AdminUser.username == payload["sub"],
        AdminUser.token == token,
        AdminUser.is_active == True
    ).first()

    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")

    return admin