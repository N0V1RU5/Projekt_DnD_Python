from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from . import models, auth, api_client
from .database import engine, get_db
from jose import JWTError, jwt
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="D&D Encounter Builder")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get current user
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(password)
    new_user = models.User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/monsters")
def list_monsters():
    return api_client.get_monsters()

@app.post("/encounters")
def create_encounter(name: str, description: str = None, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_encounter = models.Encounter(name=name, description=description, owner_id=current_user.id)
    db.add(new_encounter)
    db.commit()
    db.refresh(new_encounter)
    return new_encounter

@app.post("/encounters/{encounter_id}/add-element")
def add_element(encounter_id: int, type: str, api_index: str, name: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    encounter = db.query(models.Encounter).filter(models.Encounter.id == encounter_id, models.Encounter.owner_id == current_user.id).first()
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found")
    
    # Optional: check if count < 3 for monsters if that's a strict rule
    
    new_element = models.EncounterElement(encounter_id=encounter_id, type=type, api_index=api_index, name=name)
    db.add(new_element)
    db.commit()
    return {"message": "Element added"}

@app.get("/my-encounters")
def get_my_encounters(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Encounter).filter(models.Encounter.owner_id == current_user.id).all()

@app.get("/")
def read_root():
    return {"message": "Welcome to D&D Encounter Builder API. Go to /docs for Swagger UI."}
