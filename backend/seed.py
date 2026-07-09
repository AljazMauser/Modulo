import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models # Uvozi modele iz tvojega backend-a

SQLALCHEMY_DATABASE_URL = "sqlite:///./erp.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
models.Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

from sqlalchemy import text

# Dodaj manjkajoči stolpec zadnja_nabavna_cena v primeru, da ga SQLite ni ustvaril
try:
    db.execute(text("ALTER TABLE artikli ADD COLUMN zadnja_nabavna_cena NUMERIC(10, 2) DEFAULT 0"))
    db.commit()
    print("Dodan stolpec zadnja_nabavna_cena.")
except Exception as e:
    print("Stolpec morda že obstaja:", str(e))
    db.rollback()

# Dodaj dobavitelje
dobavitelji = [
    models.Partner(naziv="Tech-Trade d.o.o.", davcna="SI12345678", tip="dobavitelj"),
    models.Partner(naziv="Biro Oprema d.o.o.", davcna="SI87654321", tip="dobavitelj")
]

# Preveri če že obstajajo
for d in dobavitelji:
    obstaja = db.query(models.Partner).filter(models.Partner.naziv == d.naziv).first()
    if not obstaja:
        db.add(d)

# Dodaj artikle
artikli = [
    models.Artikel(sifra="M-DELL-27", naziv="Monitor Dell 27", cena=250.00, trenutna_zaloga=0, zadnja_nabavna_cena=200.00),
    models.Artikel(sifra="STOL-01", naziv="Pisarniški stol ergonomski", cena=120.00, trenutna_zaloga=0, zadnja_nabavna_cena=80.00),
    models.Artikel(sifra="KEY-LOG", naziv="Tipkovnica Logitech MX", cena=95.00, trenutna_zaloga=0, zadnja_nabavna_cena=70.00)
]

for a in artikli:
    obstaja = db.query(models.Artikel).filter(models.Artikel.sifra == a.sifra).first()
    if not obstaja:
        db.add(a)

db.commit()
print("Baza je uspešno napolnjena z začetnimi podatki!")
db.close()
