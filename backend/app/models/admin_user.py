from sqlalchemy import Column, Integer, String, Boolean
from ..db import Base

class AdminUser(Base):
    __tablename__ = 'admin_users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    token = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=True)