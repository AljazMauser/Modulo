from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
import models, schemas, auth
from database import get_db
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

router = APIRouter(
    prefix="/api",
    tags=["sales"]
)

@router.get("/partnerji", response_model=List[schemas.PartnerResponse])
def get_partnerji(db: Session = Depends(get_db), current_user: models.Uporabnik = Depends(auth.get_current_user)):
    return db.query(models.Partner).all()

@router.post("/partnerji", response_model=schemas.PartnerResponse)
def ustvari_partnerja(partner: schemas.PartnerBase, db: Session = Depends(get_db)):
    nov_partner = models.Partner(**partner.model_dump())
    db.add(nov_partner)
    db.commit()
    db.refresh(nov_partner)
    return nov_partner

@router.get("/racuni", response_model=List[schemas.RacunResponse])
def get_racuni(db: Session = Depends(get_db), current_user: models.Uporabnik = Depends(auth.require_role(['prodajalec', 'admin']))):
    return db.query(models.Racun).all()

@router.get("/racuni/{id}", response_model=schemas.RacunResponse)
def get_racun(id: int, db: Session = Depends(get_db)):
    racun = db.query(models.Racun).filter(models.Racun.id == id).first()
    if not racun:
        raise HTTPException(status_code=404, detail="Račun ne obstaja")
    return racun

@router.post("/racuni", response_model=schemas.RacunResponse)
def ustvari_racun(
    racun: schemas.RacunCreate, 
    db: Session = Depends(get_db),
    current_user: models.Uporabnik = Depends(auth.require_role(['prodajalec', 'admin']))
):
    # Preveri partnerja
    partner = db.query(models.Partner).filter(models.Partner.id == racun.partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner ne obstaja")

    # Ustvari osnovni račun
    nov_racun = models.Racun(
        stevilka_racuna=racun.stevilka_racuna,
        partner_id=racun.partner_id,
        status="osnutek",
        ustvaril_uporabnik_id=current_user.id
    )
    db.add(nov_racun)
    db.flush() # Dobimo ID računa

    skupni_znesek = 0
    # Dodaj postavke
    for postavka in racun.postavke:
        artikel = db.query(models.Artikel).filter(models.Artikel.id == postavka.artikel_id).first()
        if not artikel:
            raise HTTPException(status_code=404, detail=f"Artikel z id {postavka.artikel_id} ne obstaja")
        
        nova_postavka = models.PostavkaRacuna(
            racun_id=nov_racun.id,
            artikel_id=postavka.artikel_id,
            kolicina=postavka.kolicina,
            prodajna_cena=postavka.prodajna_cena,
            davek_procent=postavka.davek_procent
        )
        db.add(nova_postavka)
        
        # Izračun zneska (cena * količina * (1 + davek/100))
        znesek_postavke = float(postavka.prodajna_cena) * postavka.kolicina * (1 + float(postavka.davek_procent) / 100)
        skupni_znesek += znesek_postavke

    nov_racun.skupni_znesek = skupni_znesek
    db.commit()
    db.refresh(nov_racun)
    return nov_racun

@router.put("/racuni/{id}/potrdi", response_model=schemas.RacunResponse)
def potrdi_racun(
    id: int, 
    db: Session = Depends(get_db),
    current_user: models.Uporabnik = Depends(auth.require_role(['prodajalec', 'admin']))
):
    racun = db.query(models.Racun).filter(models.Racun.id == id).first()
    if not racun:
        raise HTTPException(status_code=404, detail="Račun ne obstaja")
    if racun.status != "osnutek":
        raise HTTPException(status_code=400, detail="Račun je že potrjen ali plačan")

    # Za vsako postavko kreiraj premik zaloge (izdaja) in zmanjšaj zalogo
    for postavka in racun.postavke:
        artikel = postavka.artikel
        
        if artikel.trenutna_zaloga < postavka.kolicina:
            raise HTTPException(status_code=400, detail=f"Ni dovolj zaloge za artikel: {artikel.naziv}")
            
        # Zmanjšaj zalogo
        artikel.trenutna_zaloga -= postavka.kolicina
        
        # Kreiraj premik
        premik = models.PremikZaloge(
            artikel_id=artikel.id,
            partner_id=racun.partner_id,
            kolicina=postavka.kolicina,
            tip_premika="izdaja",
            ustvaril_uporabnik_id=current_user.id
        )
        db.add(premik)

    racun.status = "potrjeno"
    db.commit()
    db.refresh(racun)
    return racun

@router.get("/racuni/{id}/pdf")
def get_racun_pdf(id: int, db: Session = Depends(get_db)):
    racun = db.query(models.Racun).filter(models.Racun.id == id).first()
    if not racun:
        raise HTTPException(status_code=404, detail="Račun ne obstaja")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Glava
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, f"RACUN st.: {racun.stevilka_racuna}")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Datum izdaje: {racun.datum_izdaje.strftime('%d.%m.%Y')}")
    p.drawString(50, height - 100, f"Partner ID: {racun.partner_id} - {racun.partner.naziv}")
    p.drawString(50, height - 120, f"Status: {racun.status.upper()}")

    # Tabela postavk - glava
    y = height - 160
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Artikel")
    p.drawString(250, y, "Kolicina")
    p.drawString(350, y, "Cena/kos")
    p.drawString(420, y, "DDV")
    p.drawString(480, y, "Skupaj")
    p.line(50, y-5, 540, y-5)
    
    # Postavke
    y -= 20
    p.setFont("Helvetica", 10)
    for postavka in racun.postavke:
        artikel_naziv = postavka.artikel.naziv if postavka.artikel else str(postavka.artikel_id)
        znesek = float(postavka.prodajna_cena) * postavka.kolicina * (1 + float(postavka.davek_procent) / 100)
        
        p.drawString(50, y, artikel_naziv[:30])
        p.drawString(250, y, str(postavka.kolicina))
        p.drawString(350, y, f"{postavka.prodajna_cena} EUR")
        p.drawString(420, y, f"{postavka.davek_procent} %")
        p.drawString(480, y, f"{znesek:.2f} EUR")
        
        y -= 20

    # Skupni znesek
    p.line(50, y, 540, y)
    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(350, y, "SKUPNI ZNESEK:")
    p.drawString(480, y, f"{racun.skupni_znesek:.2f} EUR")

    p.showPage()
    p.save()

    buffer.seek(0)
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=racun_{racun.stevilka_racuna}.pdf"}
    )

