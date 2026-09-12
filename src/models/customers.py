from src.database.database import Base
from sqlalchemy import Column, Integer, String,  DateTime
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String , nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

