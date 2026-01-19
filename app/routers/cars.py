from app.db import get_db
from app.models import Car, Dealer
from app.schemas import CarCreate, CarUpdate, CarResponse

from app.rabbitmq.producers import CarProducer

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session


def send_car_event(type: str, data: str):
    producer = CarProducer()
    producer.send_event(type, data)
    producer.close()


router = APIRouter(prefix="/api/cars", tags=["Cars"])

@router.get("/", response_model=list[CarResponse])
def get_cars(db: Session = Depends(get_db)):
    return db.query(Car).order_by(Car.id).all()

@router.get("/{id}", response_model=CarResponse)
def get_car(id: int, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Автомобиль не найден")

    return db_car

@router.post("/", response_model=CarResponse)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    create_data = car.model_dump()
    dealer = db.query(Dealer).filter(Dealer.id == create_data["dealer_id"]).first()
    if not dealer:
        raise HTTPException(status_code=400, detail="Указан неверный дилер")

    db_car = Car(**create_data)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)

    send_car_event("CREATE", create_data)

    return db_car

@router.put("/{id}", response_model=CarResponse)
def update_car(id: int, car: CarUpdate, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == id).first()
    if not db_car:
        raise HTTPException(status_code=404, detail="Автомобиль не найден")    

    update_data = car.model_dump(exclude_unset=True)

    if "dealer_id" in update_data:
        dealer = db.query(Dealer).filter(Dealer.id == update_data["dealer_id"]).first()
        if not dealer:
            raise HTTPException(status_code=400, detail="Указан неверный дилер")

    for key, value in update_data.items():
        setattr(db_car, key, value)

    db.commit()
    db.refresh(db_car)

    send_car_event("UPDATE", update_data)

    return db_car

@router.delete("/{id}")
def delete_car(id: int, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == id).first()
    if not db_car:
        raise HTTPException(status_code=404, detail="Автомобиль не найден")
    
    db.delete(db_car)
    db.commit()

    car_data = CarResponse.model_validate(db_car).model_dump(exclude={"id"})
    send_car_event("DELETE", car_data)

    return {"detail": "Автомобиль удален"}
