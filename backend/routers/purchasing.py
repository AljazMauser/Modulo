from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, auth
from database import get_db

router = APIRouter(
    prefix="/api/nabava",
    tags=["purchasing"]
)

@router.get("/", response_model=List[schemas.NabavnoNarociloResponse])
def get_narocila(db: Session = Depends(get_db), current_user: models.Uporabnik = Depends(auth.require_role(['skladiscnik', 'admin']))):
    return db.query(models.NabavnoNarocilo).all()

@router.post("/", response_model=schemas.NabavnoNarociloResponse)
def ustvari_narocilo(
    narocilo: schemas.NabavnoNarociloCreate, 
    db: Session = Depends(get_db),
    current_user: models.Uporabnik = Depends(auth.require_role(['skladiscnik', 'admin']))
):
    partner = db.query(models.Partner).filter(models.Partner.id == narocilo.partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner ne obstaja")

    nov_narocilo = models.NabavnoNarocilo(
        stevilka_narocila=narocilo.stevilka_narocila,
        partner_id=narocilo.partner_id,
        status="odprto",
        ustvaril_uporabnik_id=current_user.id
    )
    db.add(nov_narocilo)
    db.flush()

    for postavka in narocilo.postavke:
        artikel = db.query(models.Artikel).filter(models.Artikel.id == postavka.artikel_id).first()
        if not artikel:
            raise HTTPException(status_code=404, detail=f"Artikel z id {postavka.artikel_id} ne obstaja")
        
        nova_postavka = models.PostavkaNabave(
            narocilo_id=nov_narocilo.id,
            artikel_id=postavka.artikel_id,
            kolicina=postavka.kolicina,
            nabavna_cena=postavka.nabavna_cena
        )
        db.add(nova_postavka)

    db.commit()
    db.refresh(nov_narocilo)
    return nov_narocilo

@router.put("/{id}/potrdi_prejem", response_model=schemas.NabavnoNarociloResponse)
def potrdi_prejem(
    id: int, 
    db: Session = Depends(get_db),
    current_user: models.Uporabnik = Depends(auth.require_role(['skladiscnik', 'admin']))
):
    narocilo = db.query(models.NabavnoNarocilo).filter(models.NabavnoNarocilo.id == id).first()
    if not narocilo:
        raise HTTPException(status_code=404, detail="Naročilo ne obstaja")
    if narocilo.status != "odprto":
        raise HTTPException(status_code=400, detail="Naročilo je že prejeto")

    for postavka in narocilo.postavke:
        artikel = postavka.artikel
        
        # Povečaj zalogo
        artikel.trenutna_zaloga += postavka.kolicina
        
        # Posodobi zadnjo nabavno ceno
        artikel.zadnja_nabavna_cena = postavka.nabavna_cena
        
        # Kreiraj premik
        premik = models.PremikZaloge(
            artikel_id=artikel.id,
            partner_id=narocilo.partner_id,
            kolicina=postavka.kolicina,
            tip_premika="prevzem",
            ustvaril_uporabnik_id=current_user.id
        )
        db.add(premik)

    narocilo.status = "prejeto"
    db.commit()
    db.refresh(narocilo)
    return narocilo
