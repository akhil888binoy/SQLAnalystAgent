from src.database.database import Base
from sqlalchemy import Column, Integer, String,  DateTime , ForeignKey
from datetime import datetime

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)

