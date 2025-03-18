from database.db import Base
from sqlalchemy import Column, Integer, String, DateTime, UUID


class User(Base):
    __tablename__ = "users"

    uid = Column(String(36), primary_key=True, index=True)
    mobile = Column(String(20))
    firstName = Column(String(50))
    lastName = Column(String(50))
    creationTime = Column(String(90), nullable=False)
    lastUpdated = Column(String(80), nullable=True)
