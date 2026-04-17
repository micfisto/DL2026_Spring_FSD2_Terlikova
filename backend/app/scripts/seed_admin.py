from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models.admin_user import AdminUser
from ..utils.security.password import hash_password


def create_admin(db: Session):
    existing = db.query(AdminUser).filter_by(username="admin").first()

    if existing:
        print("Admin already exists")
        return

    admin = AdminUser(
        username="admin",
        email="admin@test.com",
        password=hash_password("123456"),
        is_active=True
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print("Admin created successfully")
    print("username: admin")
    print("password: 123456")


if __name__ == "__main__":
    db = SessionLocal()
    create_admin(db)
    db.close()