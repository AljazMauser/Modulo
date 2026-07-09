#!/bin/bash
# Počakaj, da se baza popolnoma zažene (opcijsko, uvicorn bo retryal ali pa seed skripta)
sleep 5 

# Poženi seed skripto, ki ustvari tabele in napolni bazo, če je še prazna
python seed_docker.py

# Zaženi Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
