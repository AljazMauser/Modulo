import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import models

engine = create_engine("sqlite:///./erp.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Add dobavitelj_id to artikli
try:
    db.execute(text("ALTER TABLE artikli ADD COLUMN dobavitelj_id INTEGER REFERENCES partnerji(id)"))
    db.commit()
    print("Column dobavitelj_id added.")
except Exception as e:
    print("Column already exists or error:", e)
    db.rollback()

# Assign existing articles to the first supplier if available
tech_trade = db.query(models.Partner).filter(models.Partner.naziv == "Tech-Trade d.o.o.").first()
biro_oprema = db.query(models.Partner).filter(models.Partner.naziv == "Biro Oprema d.o.o.").first()

if tech_trade:
    db.execute(text(f"UPDATE artikli SET dobavitelj_id = {tech_trade.id} WHERE sifra = 'M-DELL-27'"))
if biro_oprema:
    db.execute(text(f"UPDATE artikli SET dobavitelj_id = {biro_oprema.id} WHERE sifra IN ('STOL-01', 'KEY-LOG')"))

db.commit()
print("Migration completed.")
db.close()
