from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, auth
from database import get_db

router = APIRouter(
    prefix="/api",
    tags=["inventory"]
)

@router.get("/artikli", response_model=List[schemas.ArtikelResponse])
def get_artikli(db: Session = Depends(get_db), current_user: models.Uporabnik = Depends(auth.get_current_user)):
    artikli = db.query(models.Artikel).all()
    return artikli

@router.post("/premiki", response_model=schemas.PremikZalogeResponse)
def ustvari_premik(
    premik: schemas.PremikZalogeCreate, 
    db: Session = Depends(get_db),
    current_user: models.Uporabnik = Depends(auth.require_role(['skladiscnik', 'admin']))
):
    # Preverimo artikel
    artikel = db.query(models.Artikel).filter(models.Artikel.id == premik.artikel_id).first()
    if not artikel:
        raise HTTPException(status_code=404, detail="Artikel ne obstaja")
    
    # Validacija tipa premika in zaloge
    if premik.tip_premika not in ['prevzem', 'izdaja']:
        raise HTTPException(status_code=400, detail="Neveljaven tip premika")
        
    if premik.tip_premika == 'izdaja' and artikel.trenutna_zaloga < premik.kolicina:
        raise HTTPException(status_code=400, detail="Ni dovolj zaloge za izdajo")

    # Ustvarimo premik
    nov_premik = models.PremikZaloge(
        artikel_id=premik.artikel_id,
        partner_id=premik.partner_id,
        kolicina=premik.kolicina,
        tip_premika=premik.tip_premika,
        ustvaril_uporabnik_id=current_user.id
    )
    db.add(nov_premik)

    # Posodobimo trenutno zalogo v tabeli artikli
    if premik.tip_premika == 'prevzem':
        artikel.trenutna_zaloga += premik.kolicina
    elif premik.tip_premika == 'izdaja':
        artikel.trenutna_zaloga -= premik.kolicina

    db.commit()
    db.refresh(nov_premik)
    return nov_premik

@router.post("/artikli", response_model=schemas.ArtikelResponse)
def ustvari_artikel(
    artikel: schemas.ArtikelCreate, 
    db: Session = Depends(get_db),
    current_user: models.Uporabnik = Depends(auth.require_role(['skladiscnik', 'admin']))
):
    db_artikel = db.query(models.Artikel).filter(models.Artikel.sifra == artikel.sifra).first()
    if db_artikel:
        raise HTTPException(status_code=400, detail="Artikel s to šifro že obstaja")
    
    nov_artikel = models.Artikel(**artikel.model_dump())
    db.add(nov_artikel)
    db.commit()
    db.refresh(nov_artikel)
    return nov_artikel

@router.get("/artikli/{id}/premiki", response_model=List[schemas.PremikZalogeResponse])
def get_premiki_artikla(
    id: int, 
    db: Session = Depends(get_db),
    current_user: models.Uporabnik = Depends(auth.get_current_user)
):
    artikel = db.query(models.Artikel).filter(models.Artikel.id == id).first()
    if not artikel:
        raise HTTPException(status_code=404, detail="Artikel ne obstaja")
    
    premiki = db.query(models.PremikZaloge)\
                .filter(models.PremikZaloge.artikel_id == id)\
                .order_by(models.PremikZaloge.datum.desc())\
                .all()
    return premiki

