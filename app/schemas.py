from pydantic import BaseModel
from typing import Optional


# Cars

class CarBase(BaseModel):
    firm: str
    model: str
    year: int
    power: int
    color: str
    price: int
    dealer_id: int


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    firm: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    power: Optional[int] = None
    color: Optional[str] = None
    price: Optional[int] = None
    dealer_id: Optional[int] = None


class CarResponse(CarBase):
    id: int

    class Config:
        from_attributes = True


# Dealers

class DealerBase(BaseModel):
    name: str
    city: str
    address: str
    area: str
    rating: float


class DealerCreate(DealerBase):
    pass


class DealerUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    area: Optional[str] = None
    rating: Optional[float] = None


class DealerResponse(DealerBase):
    id: int

    class Config:
        from_attributes = True
