from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relation

from datetime import datetime


Base = declarative_base()


class Customer(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    phone_number = Column(String, unique=True, index=True)
    
    orders = relation('Order', back_populates='customer')


class Restaurant(Base):
    __tablename__ = 'restaurants'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    name = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    serve_area = Column(Integer, nullable=False)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    menu = relation('Product', back_populates='restaurant')
    orders = relation('Order', back_populates='restaurant')
    couriers = relation('Courier', back_populates='restaurant')
    
    
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    
    restaurant = relation(Restaurant, back_populates='menu')
    order_items = relation('OrderItem', back_populates='product')
    
    
class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))

    count = Column(Integer, nullable=False)

    product = relation(Product, back_populates='order_items')
    order = relation('Order', back_populates='order_items')

    
class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('users.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    
    description = Column(String, nullable=True, default='')
    destination = Column(String, nullable=False)
    state = Column(String, default='В обработке')
    date = Column(DateTime, default=datetime.now)
    
    customer = relation(Customer, back_populates='orders')
    restaurant = relation(Restaurant, back_populates='orders')
    order_items = relation(OrderItem, back_populates='order')
    courier = relation('Courier', back_populates='order')


class Courier(Base):
    __tablename__ = 'couriers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)

    vk_id = Column(Integer, nullable=False, unique=True)
    verified = Column(Integer, nullable=False, default=False)
    address = Column(String, nullable=True)
    working = Column(Boolean, nullable=False, default=False)
    notified = Column(Boolean, nullable=False, default=False)

    order = relation(Order, back_populates='courier')
    restaurant = relation(Restaurant, back_populates='couriers')
