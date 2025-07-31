from sqlalchemy import Column, Integer, String, Boolean, Date
from db.session import Base
from datetime import datetime

class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(Date, default=datetime.utcnow)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)