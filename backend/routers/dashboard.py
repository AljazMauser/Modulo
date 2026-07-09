from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import calendar
import models, auth
from database import get_db

router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"]
)

@router.get("/kpi")
def get_kpi(db: Session = Depends(get_db), current_user: models.Uporabnik = Depends(auth.get_current_user)):
    # 1. Skupna vrednost zaloge v skladišču (cena * zaloga)
    # Using 'zadnja_nabavna_cena' or 'cena'? Usually inventory value is based on purchase price (zadnja_nabavna_cena).
    # We will use sum(zadnja_nabavna_cena * trenutna_zaloga). If not available, fallback to cena.
    zalog_items = db.query(models.Artikel.trenutna_zaloga, models.Artikel.zadnja_nabavna_cena).filter(models.Artikel.trenutna_zaloga > 0).all()
    skupna_vrednost = sum(item[0] * float(item[1] or 0) for item in zalog_items)

    # 2. Prihodki ta mesec
    now = datetime.now()
    first_day_of_month = datetime(now.year, now.month, 1)
    
    prihodki = db.query(func.sum(models.Racun.skupni_znesek)).filter(
        models.Racun.status.in_(['potrjeno', 'placano']),
        models.Racun.datum_izdaje >= first_day_of_month
    ).scalar() or 0

    # 3. Število neplačanih računov (potrjeno = issued but not paid)
    neplacani = db.query(func.count(models.Racun.id)).filter(models.Racun.status == 'potrjeno').scalar() or 0

    return {
        "vrednost_zaloge": skupna_vrednost,
        "prihodki_mesec": prihodki,
        "neplacani_racuni": neplacani
    }

@router.get("/charts")
def get_charts(db: Session = Depends(get_db), current_user: models.Uporabnik = Depends(auth.get_current_user)):
    # 1. Monthly revenue (last 6 months)
    now = datetime.now()
    monthly_revenue = {"labels": [], "data": []}
    
    for i in range(5, -1, -1):
        m = now.month - i
        y = now.year
        if m <= 0:
            m += 12
            y -= 1
        
        start_date = datetime(y, m, 1)
        _, last_day = calendar.monthrange(y, m)
        end_date = datetime(y, m, last_day, 23, 59, 59)
        
        revenue = db.query(func.sum(models.Racun.skupni_znesek)).filter(
            models.Racun.status.in_(['potrjeno', 'placano']),
            models.Racun.datum_izdaje >= start_date,
            models.Racun.datum_izdaje <= end_date
        ).scalar() or 0
        
        monthly_revenue["labels"].append(f"{m:02d}/{y}")
        monthly_revenue["data"].append(float(revenue))
        
    # 2. Top 5 najbolj prodajanih artiklov
    top_items = db.query(
        models.Artikel.naziv, 
        func.sum(models.PostavkaRacuna.kolicina).label('total_qty')
    ).join(models.PostavkaRacuna, models.Artikel.id == models.PostavkaRacuna.artikel_id)\
     .group_by(models.Artikel.id)\
     .order_by(func.sum(models.PostavkaRacuna.kolicina).desc())\
     .limit(5).all()

    top_products = {
        "labels": [item.naziv for item in top_items],
        "data": [item.total_qty for item in top_items]
    }

    return {
        "monthly_revenue": monthly_revenue,
        "top_products": top_products
    }
