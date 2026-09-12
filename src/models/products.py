from src.database.database import Base
from sqlalchemy import Column, Integer, String,  DateTime
from datetime import datetime

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String , nullable=False)
    price = Column(Integer, nullable=False)

