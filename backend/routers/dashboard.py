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

from typing import Optional

@router.get("/kpi")
def get_kpi(
    period: str = "this_month", 
    db: Session = Depends(get_db), 
    current_user: models.Uporabnik = Depends(auth.require_role(['admin']))
):
    now = datetime.now()
    if period == "90days":
        start_date = now - timedelta(days=90)
    elif period == "this_year":
        start_date = datetime(now.year, 1, 1)
    else:
        start_date = datetime(now.year, now.month, 1)

    # 1. Skupna vrednost zaloge (se ne spreminja glede na filter, vedno je trenutna vrednost)
    zalog_items = db.query(models.Artikel.trenutna_zaloga, models.Artikel.zadnja_nabavna_cena).filter(models.Artikel.trenutna_zaloga > 0).all()
    skupna_vrednost = sum(item[0] * float(item[1] or 0) for item in zalog_items)

    # 2. Prihodki v obdobju
    prihodki = db.query(func.sum(models.Racun.skupni_znesek)).filter(
        models.Racun.status.in_(['potrjeno', 'placano']),
        models.Racun.datum_izdaje >= start_date
    ).scalar() or 0

    # 3. Število neplačanih računov (v obdobju)
    neplacani = db.query(func.count(models.Racun.id)).filter(
        models.Racun.status == 'potrjeno',
        models.Racun.datum_izdaje >= start_date
    ).scalar() or 0

    return {
        "vrednost_zaloge": skupna_vrednost,
        "prihodki_mesec": prihodki,
        "neplacani_racuni": neplacani
    }

@router.get("/charts")
def get_charts(
    period: str = "this_month", 
    db: Session = Depends(get_db), 
    current_user: models.Uporabnik = Depends(auth.require_role(['admin']))
):
    now = datetime.now()
    
    # Določi začetni datum in število mesecev za graf
    if period == "90days":
        start_date = now - timedelta(days=90)
        months_to_show = 3
    elif period == "this_year":
        start_date = datetime(now.year, 1, 1)
        months_to_show = now.month
    else:
        start_date = datetime(now.year, now.month, 1)
        months_to_show = 6 # Pri 'ta mesec' vseeno pokažemo zadnjih 6 mesecev za lažjo primerjavo na grafu
        
    monthly_revenue = {"labels": [], "data": []}
    
    # Generiraj mesečne podatke za graf
    for i in range(months_to_show - 1, -1, -1):
        m = now.month - i
        y = now.year
        if m <= 0:
            m += 12
            y -= 1
        
        m_start_date = datetime(y, m, 1)
        _, last_day = calendar.monthrange(y, m)
        m_end_date = datetime(y, m, last_day, 23, 59, 59)
        
        revenue = db.query(func.sum(models.Racun.skupni_znesek)).filter(
            models.Racun.status.in_(['potrjeno', 'placano']),
            models.Racun.datum_izdaje >= m_start_date,
            models.Racun.datum_izdaje <= m_end_date
        ).scalar() or 0
        
        monthly_revenue["labels"].append(f"{m:02d}/{y}")
        monthly_revenue["data"].append(float(revenue))
        
    # 2. Top 5 najbolj prodajanih artiklov v obdobju
    top_items = db.query(
        models.Artikel.naziv, 
        func.sum(models.PostavkaRacuna.kolicina).label('total_qty')
    ).join(models.PostavkaRacuna, models.Artikel.id == models.PostavkaRacuna.artikel_id)\
     .join(models.Racun, models.Racun.id == models.PostavkaRacuna.racun_id)\
     .filter(models.Racun.datum_izdaje >= start_date)\
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
