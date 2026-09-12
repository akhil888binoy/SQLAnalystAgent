from src.database.database import Base
from sqlalchemy import Column, Integer, String,  DateTime , ForeignKey
from datetime import datetime

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)

