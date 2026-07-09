from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import inventory, sales, purchasing, auth_router, users
import models

# Kreacija tabel iz modelov, če še ne obstajajo
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Modulo API",
    description="Osnovni API za nas po meri narejen ERP sistem.",
    version="0.1.0"
)

# CORS nastavitve (Nuxt 3 bo privzeto tekel na localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Vključitev routerjev
app.include_router(auth_router.router)
app.include_router(users.router)
app.include_router(inventory.router)
app.include_router(sales.router)
app.include_router(purchasing.router)

@app.get("/")
def read_root():
    return {"message": "Dobrodošli v Modulo API. Pojdite na /docs za Swagger dokumentacijo."}
