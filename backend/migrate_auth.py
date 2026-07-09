import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import models
import auth

engine = create_engine("sqlite:///./erp.db", connect_args={"check_same_thread": False})
models.Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Add ustvaril_uporabnik_id columns
tables = ['premiki_zaloge', 'racuni', 'nabavna_narocila']
for table in tables:
    try:
        db.execute(text(f"ALTER TABLE {table} ADD COLUMN ustvaril_uporabnik_id INTEGER REFERENCES uporabniki(id)"))
        db.commit()
        print(f"Column ustvaril_uporabnik_id added to {table}.")
    except Exception as e:
        print(f"Column already exists in {table} or error:", e)
        db.rollback()

# Seed admin user
admin = db.query(models.Uporabnik).filter(models.Uporabnik.email == "admin@erp.com").first()
if not admin:
    hashed_password = auth.get_password_hash("admin123")
    admin = models.Uporabnik(
        ime="Admin",
        priimek="Sistem",
        email="admin@erp.com",
        geslo_hash=hashed_password,
        vloga="admin"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print("Admin user created.")

# Optionally update existing records to belong to admin
for table in tables:
    db.execute(text(f"UPDATE {table} SET ustvaril_uporabnik_id = NULL WHERE ustvaril_uporabnik_id IS NULL"))

db.commit()
print("Auth migration completed.")
db.close()
