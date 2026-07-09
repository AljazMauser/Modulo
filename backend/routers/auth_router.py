from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import models, schemas, auth, database

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Uporabnik).filter(models.Uporabnik.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.geslo_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.vloga}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": {"id": user.id, "ime": user.ime, "priimek": user.priimek, "email": user.email, "vloga": user.vloga}}
