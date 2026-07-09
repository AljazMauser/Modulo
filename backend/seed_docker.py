import time
from sqlalchemy.exc import OperationalError
from database import engine, SessionLocal
import models
import auth

def wait_for_db():
    retries = 5
    while retries > 0:
        try:
            # Try to connect to ensure DB is ready
            conn = engine.connect()
            conn.close()
            print("Povezava z bazo uspešna.")
            return True
        except OperationalError:
            retries -= 1
            print(f"Baza še ni pripravljena, ponovni poskus... ({retries} preostalih)")
            time.sleep(3)
    return False

def seed_database():
    if not wait_for_db():
        print("Ne morem se povezati na bazo. Prekinjam seed.")
        return

    # Ustvari tabele, če ne obstajajo
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Dodaj Admina
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
            print("Dodan začetni Admin (admin@erp.com).")

        # 2. Dodaj Dobavitelje
        dobavitelji = [
            models.Partner(naziv="Tech-Trade d.o.o.", davcna="SI12345678", tip="dobavitelj"),
            models.Partner(naziv="Biro Oprema d.o.o.", davcna="SI87654321", tip="dobavitelj")
        ]
        
        for d in dobavitelji:
            obstaja = db.query(models.Partner).filter(models.Partner.naziv == d.naziv).first()
            if not obstaja:
                db.add(d)
                print(f"Dodan dobavitelj: {d.naziv}")

        # 3. Dodaj Artikle
        artikli = [
            models.Artikel(sifra="M-DELL-27", naziv="Monitor Dell 27", cena=250.00, trenutna_zaloga=0, zadnja_nabavna_cena=200.00),
            models.Artikel(sifra="STOL-01", naziv="Pisarniški stol ergonomski", cena=120.00, trenutna_zaloga=0, zadnja_nabavna_cena=80.00),
            models.Artikel(sifra="KEY-LOG", naziv="Tipkovnica Logitech MX", cena=95.00, trenutna_zaloga=0, zadnja_nabavna_cena=70.00)
        ]

        for a in artikli:
            obstaja = db.query(models.Artikel).filter(models.Artikel.sifra == a.sifra).first()
            if not obstaja:
                db.add(a)
                print(f"Dodan artikel: {a.naziv}")

        db.commit()
        print("Baza uspešno inicializirana s testnimi podatki!")

    except Exception as e:
        print("Napaka pri polnjenju baze:", str(e))
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
