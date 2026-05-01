from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, api_client
from .database import engine, get_db

# vytvoreni tabulek v db pri startu
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="dnd notebook")
templates = Jinja2Templates(directory="app/templates")

# ziskani uzivatele z cookies
def get_logged_user(request: Request, db: Session = Depends(get_db)):
    username = request.cookies.get("username")
    if not username:
        return None
    return db.query(models.User).filter(models.User.username == username).first()

@app.get("/", response_class=HTMLResponse)
def index(request: Request, user = Depends(get_logged_user)):
    return templates.TemplateResponse(request=request, name="base.html", context={"user": user})

# jednoduchy login a registrace v jednom
@app.post("/login")
def login(username: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        user = models.User(username=username, password="password")
        db.add(user)
        db.commit()
    
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="username", value=username)
    return response

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("username")
    return response

# vypis monster
@app.get("/monsters", response_class=HTMLResponse)
def list_monsters(request: Request, user = Depends(get_logged_user)):
    items = api_client.get_monsters()
    return templates.TemplateResponse(request=request, name="list.html", context={
        "items": items, "category": "Monsters", "category_slug": "monsters", "user": user
    })

# vypis kouzel
@app.get("/spells", response_class=HTMLResponse)
def list_spells(request: Request, user = Depends(get_logged_user)):
    items = api_client.get_spells()
    return templates.TemplateResponse(request=request, name="list.html", context={
        "items": items, "category": "Spells", "category_slug": "spells", "user": user
    })

# detail polozky z api
@app.get("/detail/{category}/{index}", response_class=HTMLResponse)
def detail(request: Request, category: str, index: str, user = Depends(get_logged_user)):
    data = api_client.get_details(category, index)
    return templates.TemplateResponse(request=request, name="detail.html", context={
        "detail": data, "category_slug": category, "user": user
    })

# pridani do oblibenych
@app.post("/add-favorite")
def add_favorite(type: str = Form(...), api_index: str = Form(...), name: str = Form(...), db: Session = Depends(get_db), user = Depends(get_logged_user)):
    if not user:
        return RedirectResponse(url="/", status_code=303)
    
    enc = db.query(models.Encounter).filter(models.Encounter.owner_id == user.id).first()
    if not enc:
        enc = models.Encounter(name="Favorites", owner_id=user.id)
        db.add(enc)
        db.commit()
        db.refresh(enc)
    
    new_el = models.EncounterElement(encounter_id=enc.id, type=type, api_index=api_index, name=name)
    db.add(new_el)
    db.commit()
    return RedirectResponse(url="/profile", status_code=303)

# smazani z oblibenych
@app.post("/remove-favorite")
def remove_favorite(element_id: int = Form(...), db: Session = Depends(get_db), user = Depends(get_logged_user)):
    if not user:
        return RedirectResponse(url="/", status_code=303)
    
    element = db.query(models.EncounterElement).join(models.Encounter).filter(
        models.EncounterElement.id == element_id,
        models.Encounter.owner_id == user.id
    ).first()
    
    if element:
        db.delete(element)
        db.commit()
    
    return RedirectResponse(url="/profile", status_code=303)

# profil uzivatele
@app.get("/profile", response_class=HTMLResponse)
def profile(request: Request, db: Session = Depends(get_db), user = Depends(get_logged_user)):
    if not user:
        return RedirectResponse(url="/")
    elements = db.query(models.EncounterElement).join(models.Encounter).filter(models.Encounter.owner_id == user.id).all()
    return templates.TemplateResponse(request=request, name="profile.html", context={
        "user": user, "elements": elements
    })
