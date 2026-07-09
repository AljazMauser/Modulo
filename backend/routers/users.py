from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas, auth, database

router = APIRouter(
    prefix="/api/uporabniki",
    tags=["uporabniki"]
)

@router.get("/me", response_model=schemas.UporabnikResponse)
def read_users_me(current_user: models.Uporabnik = Depends(auth.get_current_user)):
    return current_user

@router.get("/", response_model=List[schemas.UporabnikResponse])
def get_uporabniki(
    db: Session = Depends(database.get_db), 
    current_user: models.Uporabnik = Depends(auth.require_role(["admin"]))
):
    return db.query(models.Uporabnik).all()

@router.post("/", response_model=schemas.UporabnikResponse)
def ustvari_uporabnika(
    user: schemas.UporabnikCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.Uporabnik = Depends(auth.require_role(["admin"]))
):
    obstaja = db.query(models.Uporabnik).filter(models.Uporabnik.email == user.email).first()
    if obstaja:
        raise HTTPException(status_code=400, detail="Uporabnik s tem e-poštnim naslovom že obstaja.")
    
    hashed_password = auth.get_password_hash(user.geslo)
    nov_uporabnik = models.Uporabnik(
        ime=user.ime,
        priimek=user.priimek,
        email=user.email,
        geslo_hash=hashed_password,
        vloga=user.vloga
    )
    db.add(nov_uporabnik)
    db.commit()
    db.refresh(nov_uporabnik)
    return nov_uporabnik
