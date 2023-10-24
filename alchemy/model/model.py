from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Schema = declarative_base()

class Product(Schema):

    __tablename__ = "products"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(80), nullable=False)
    price = Column(Float(2))

class Customer(Schema):

    __tablename__ = "customers"

    id = Column(Integer, autoincrement=True, primary_key=True)
    firstname = Column(String(80), nullable=False)
    lastname = Column(String(80), nullable=False)

class Order(Schema):

    __tablename__ = "order"

    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(DateTime, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship('Customer')

class Purchase(Schema):

    __tablename__ = 'purchase'

    quantity = Column(Integer, nullable=False)

    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    product = relationship('Product')
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    order = relationship('Order')

