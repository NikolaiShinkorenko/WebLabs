from app.db import get_db
from app.models import Dealer
from app.schemas import DealerCreate, DealerUpdate, DealerResponse

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/dealers", tags=["Dealers"])

@router.get("/", response_model=list[DealerResponse])
def get_dealers(db: Session = Depends(get_db)):
    return db.query(Dealer).order_by(Dealer.id).all()

@router.get("/{id}", response_model=DealerResponse)
def get_dealer(id: int, db: Session = Depends(get_db)):
    db_dealer = db.query(Dealer).filter(Dealer.id == id).first()
    if db_dealer is None:
        raise HTTPException(status_code=404, detail="Дилер не найден")
    return db_dealer

@router.post("/", response_model=DealerResponse)
def create_dealer(dealer: DealerCreate, db: Session = Depends(get_db)):
    db_dealer = Dealer(**dealer.model_dump())
    db.add(db_dealer)
    db.commit()
    db.refresh(db_dealer)
    return db_dealer

@router.put("/{id}", response_model=DealerResponse)
def update_dealer(id: int, dealer: DealerUpdate, db: Session = Depends(get_db)):
    db_dealer = db.query(Dealer).filter(Dealer.id == id).first()
    if db_dealer is None:
        raise HTTPException(status_code=404, detail="Дилер не найден")
    
    for key, value in dealer.model_dump(exclude_unset=True).items():
        setattr(db_dealer, key, value)
    
    db.commit()
    db.refresh(db_dealer)
    return db_dealer

@router.delete("/{id}")
def delete_dealer(id: int, db: Session = Depends(get_db)):
    db_dealer = db.query(Dealer).filter(Dealer.id == id).first()
    if not db_dealer:
        raise HTTPException(status_code=404, detail="Дилер не найден")
    
    db.delete(db_dealer)
    db.commit()
    return {"detail": "Дилер удален"}