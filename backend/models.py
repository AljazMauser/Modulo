from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Uporabnik(Base):
    __tablename__ = "uporabniki"

    id = Column(Integer, primary_key=True, index=True)
    ime = Column(String(50), nullable=False)
    priimek = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    geslo_hash = Column(String(255), nullable=False)
    vloga = Column(String(50), default="prodajalec") # 'admin', 'prodajalec', 'skladiscnik'

class Artikel(Base):
    __tablename__ = "artikli"

    id = Column(Integer, primary_key=True, index=True)
    sifra = Column(String(50), unique=True, index=True, nullable=False)
    naziv = Column(String(100), index=True, nullable=False)
    cena = Column(Numeric(10, 2), nullable=False)
    zadnja_nabavna_cena = Column(Numeric(10, 2), default=0)
    trenutna_zaloga = Column(Integer, default=0)
    dobavitelj_id = Column(Integer, ForeignKey("partnerji.id"), nullable=True)

    premiki = relationship("PremikZaloge", back_populates="artikel")
    dobavitelj = relationship("Partner")

class Partner(Base):
    __tablename__ = "partnerji"

    id = Column(Integer, primary_key=True, index=True)
    naziv = Column(String(255), nullable=False)
    davcna = Column(String(50))
    tip = Column(String(50), nullable=False) # 'dobavitelj', 'stranka'

    premiki = relationship("PremikZaloge", back_populates="partner")

class PremikZaloge(Base):
    __tablename__ = "premiki_zaloge"

    id = Column(Integer, primary_key=True, index=True)
    artikel_id = Column(Integer, ForeignKey("artikli.id"))
    partner_id = Column(Integer, ForeignKey("partnerji.id"))
    kolicina = Column(Integer, nullable=False)
    tip_premika = Column(String(50), nullable=False) # 'prevzem', 'izdaja'
    datum = Column(DateTime(timezone=True), server_default=func.now())
    ustvaril_uporabnik_id = Column(Integer, ForeignKey("uporabniki.id"), nullable=True)

    artikel = relationship("Artikel", back_populates="premiki")
    partner = relationship("Partner", back_populates="premiki")
    ustvaril_uporabnik = relationship("Uporabnik")

class Racun(Base):
    __tablename__ = "racuni"

    id = Column(Integer, primary_key=True, index=True)
    stevilka_racuna = Column(String(50), unique=True, index=True, nullable=False)
    partner_id = Column(Integer, ForeignKey("partnerji.id"), nullable=False)
    datum_izdaje = Column(DateTime(timezone=True), server_default=func.now())
    skupni_znesek = Column(Numeric(10, 2), default=0)
    status = Column(String(50), default='osnutek') # 'osnutek', 'potrjeno', 'placano'
    ustvaril_uporabnik_id = Column(Integer, ForeignKey("uporabniki.id"), nullable=True)

    partner = relationship("Partner")
    postavke = relationship("PostavkaRacuna", back_populates="racun", cascade="all, delete-orphan")
    ustvaril_uporabnik = relationship("Uporabnik")

class PostavkaRacuna(Base):
    __tablename__ = "postavke_racuna"

    id = Column(Integer, primary_key=True, index=True)
    racun_id = Column(Integer, ForeignKey("racuni.id"), nullable=False)
    artikel_id = Column(Integer, ForeignKey("artikli.id"), nullable=False)
    kolicina = Column(Integer, nullable=False)
    prodajna_cena = Column(Numeric(10, 2), nullable=False)
    davek_procent = Column(Numeric(5, 2), default=22.0)

    racun = relationship("Racun", back_populates="postavke")
    artikel = relationship("Artikel")

class NabavnoNarocilo(Base):
    __tablename__ = "nabavna_narocila"

    id = Column(Integer, primary_key=True, index=True)
    stevilka_narocila = Column(String(50), unique=True, index=True, nullable=False)
    partner_id = Column(Integer, ForeignKey("partnerji.id"), nullable=False)
    datum_narocila = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default='odprto') # 'odprto', 'prejeto'
    ustvaril_uporabnik_id = Column(Integer, ForeignKey("uporabniki.id"), nullable=True)

    partner = relationship("Partner")
    postavke = relationship("PostavkaNabave", back_populates="narocilo", cascade="all, delete-orphan")
    ustvaril_uporabnik = relationship("Uporabnik")

class PostavkaNabave(Base):
    __tablename__ = "postavke_nabave"

    id = Column(Integer, primary_key=True, index=True)
    narocilo_id = Column(Integer, ForeignKey("nabavna_narocila.id"), nullable=False)
    artikel_id = Column(Integer, ForeignKey("artikli.id"), nullable=False)
    kolicina = Column(Integer, nullable=False)
    nabavna_cena = Column(Numeric(10, 2), nullable=False)

    narocilo = relationship("NabavnoNarocilo", back_populates="postavke")
    artikel = relationship("Artikel")
