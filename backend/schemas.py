from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# --- Uporabniki in Avtentikacija ---
class UporabnikBase(BaseModel):
    ime: str
    priimek: str
    email: str
    vloga: str = "prodajalec"

class UporabnikCreate(UporabnikBase):
    geslo: str

class UporabnikResponse(UporabnikBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UporabnikResponse

class TokenData(BaseModel):
    email: Optional[str] = None
    vloga: Optional[str] = None

# --- Artikel ---
class ArtikelBase(BaseModel):
    sifra: str
    naziv: str
    cena: float
    zadnja_nabavna_cena: float = 0.0
    dobavitelj_id: Optional[int] = None

class ArtikelCreate(ArtikelBase):
    pass

class ArtikelResponse(ArtikelBase):
    id: int
    trenutna_zaloga: int
    model_config = ConfigDict(from_attributes=True)

# --- Partner ---
class PartnerBase(BaseModel):
    naziv: str
    davcna: Optional[str] = None
    tip: str

class PartnerResponse(PartnerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Premik Zaloge ---
class PremikZalogeCreate(BaseModel):
    artikel_id: int
    partner_id: Optional[int] = None
    kolicina: int
    tip_premika: str # 'prevzem' ali 'izdaja'

class PremikZalogeResponse(PremikZalogeCreate):
    id: int
    datum: datetime
    ustvaril_uporabnik_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

# --- Račun ---
class PostavkaRacunaBase(BaseModel):
    artikel_id: int
    kolicina: int
    prodajna_cena: float
    davek_procent: float = 22.0

class PostavkaRacunaCreate(PostavkaRacunaBase):
    pass

class PostavkaRacunaResponse(PostavkaRacunaBase):
    id: int
    racun_id: int
    model_config = ConfigDict(from_attributes=True)

class RacunBase(BaseModel):
    stevilka_racuna: str
    partner_id: int

class RacunCreate(RacunBase):
    postavke: List[PostavkaRacunaCreate]

class RacunResponse(RacunBase):
    id: int
    datum_izdaje: datetime
    skupni_znesek: float
    status: str
    ustvaril_uporabnik_id: Optional[int] = None
    postavke: List[PostavkaRacunaResponse] = []
    model_config = ConfigDict(from_attributes=True)

# --- Nabava ---
class PostavkaNabaveBase(BaseModel):
    artikel_id: int
    kolicina: int
    nabavna_cena: float

class PostavkaNabaveCreate(PostavkaNabaveBase):
    pass

class PostavkaNabaveResponse(PostavkaNabaveBase):
    id: int
    narocilo_id: int
    model_config = ConfigDict(from_attributes=True)

class NabavnoNarociloBase(BaseModel):
    stevilka_narocila: str
    partner_id: int

class NabavnoNarociloCreate(NabavnoNarociloBase):
    postavke: List[PostavkaNabaveCreate]

class NabavnoNarociloResponse(NabavnoNarociloBase):
    id: int
    datum_narocila: datetime
    status: str
    ustvaril_uporabnik_id: Optional[int] = None
    postavke: List[PostavkaNabaveResponse] = []
    model_config = ConfigDict(from_attributes=True)
