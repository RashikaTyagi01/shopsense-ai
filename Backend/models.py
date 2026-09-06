from sqlalchemy import Column,Integer,String,Float
from database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    description = Column(String)
    price=Column(Float)
    quantity=Column(Integer)
    category=Column(String)
    delivery_days=Column(Integer)


class PurchaseHistory(Base):
    __tablename__= "purchase_history"

    id=Column(Integer, primary_key=True)
    user_id=Column(Integer)
    product_id=Column(Integer)
    quantity=Column(Integer)
    purchase_date=Column(String)

class CartItem(Base):
    __tablename__ ="cart_items"
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer)
    product_id=Column(Integer)
    quantity=Column(Integer)
    

