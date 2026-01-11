from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Dealer(Base):
    __tablename__ = 'dealers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String, nullable=False)
    area = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    
    cars = relationship("Car", back_populates="dealer")


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firm = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    power = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    
    dealer_id = Column(Integer, ForeignKey("dealers.id"))
    dealer = relationship("Dealer", back_populates="cars")

