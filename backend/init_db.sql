CREATE TABLE IF NOT EXISTS artikli (
    id SERIAL PRIMARY KEY,
    sifra VARCHAR(50) UNIQUE NOT NULL,
    naziv VARCHAR(255) NOT NULL,
    cena DECIMAL(10, 2) NOT NULL,
    trenutna_zaloga INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS partnerji (
    id SERIAL PRIMARY KEY,
    naziv VARCHAR(255) NOT NULL,
    davcna VARCHAR(50),
    tip VARCHAR(50) CHECK (tip IN ('dobavitelj', 'stranka')) NOT NULL
);

CREATE TABLE IF NOT EXISTS premiki_zaloge (
    id SERIAL PRIMARY KEY,
    artikel_id INTEGER REFERENCES artikli(id),
    partner_id INTEGER REFERENCES partnerji(id),
    kolicina INTEGER NOT NULL,
    tip_premika VARCHAR(50) CHECK (tip_premika IN ('prevzem', 'izdaja')) NOT NULL,
    datum TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
