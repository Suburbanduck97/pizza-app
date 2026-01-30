import os
from dotenv import load_dotenv 
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import random
from . import models, database


load_dotenv()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")


if not ADMIN_PASSWORD or not SECRET_TOKEN:
    print("⚠️ AVISO: Variáveis de ambiente ADMIN_PASSWORD ou SECRET_TOKEN não configuradas!")

app = FastAPI(title="Bibi Pizza API")

#  CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos (Frontend)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Banco verificacao
class SizeUpdate(BaseModel):
    price: float

class FlavorUpdate(BaseModel):
    active: bool

class LoginRequest(BaseModel):
    password: str

# seguranca
def verify_admin(x_token: str = Header(...)):
    if x_token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")

# --- ROTAS DE LOGIN ---
@app.post("/api/login")
def login(data: LoginRequest):
    if data.password == ADMIN_PASSWORD:
        return {"token": SECRET_TOKEN}
    raise HTTPException(status_code=401, detail="Senha incorreta")

# --- ROTAS PÚBLICAS ---
@app.get("/api/menu")
def get_menu(db: Session = Depends(get_db)):
    sizes = db.query(models.Size).all()
    flavors = db.query(models.Flavor).all()
    beverages = db.query(models.Beverage).filter(models.Beverage.active == True).all()
    
    menu_flavors = {}
    for f in flavors:
        cat_name = f.category.name
        if cat_name not in menu_flavors:
            menu_flavors[cat_name] = []
        menu_flavors[cat_name].append({
            "id": f.id,
            "name": f.name,
            "description": f.description,
            "active": f.active 
        })
    return {"sizes": sizes, "flavors": menu_flavors, "beverages": beverages}

@app.get("/api/suggest/{size_id}")
def suggest_flavors(size_id: int, db: Session = Depends(get_db)):
    size = db.query(models.Size).get(size_id)
    if not size:
        raise HTTPException(status_code=404, detail="Tamanho não encontrado")
    
    savory = db.query(models.Flavor).join(models.Category).filter(
        models.Flavor.active == True, 
        models.Category.name == "Tradicional"
    ).all()
    
    limit = min(size.max_flavors, 3)
    suggestions = []

    for _ in range(2):
        if len(savory) >= limit:
            selected = random.sample(savory, limit)
            names = [f.name.split(" ")[1] if f.name[0].isdigit() else f.name for f in selected]
            suggestions.append({
                "ids": [f.id for f in selected],
                "names": [f.name for f in selected],
                "title": f"Combo: {', '.join(names)}"
            })
    return suggestions

# --- ROTAS PROTEGIDAS (Admin) ---
@app.put("/api/admin/sizes/{size_id}", dependencies=[Depends(verify_admin)])
def update_size_price(size_id: int, item: SizeUpdate, db: Session = Depends(get_db)):
    size = db.query(models.Size).get(size_id)
    if not size:
        raise HTTPException(status_code=404, detail="Tamanho não encontrado")
    size.price = item.price
    db.commit()
    return {"message": "Preço atualizado"}

@app.put("/api/admin/flavors/{flavor_id}", dependencies=[Depends(verify_admin)])
def toggle_flavor(flavor_id: int, item: FlavorUpdate, db: Session = Depends(get_db)):
    flavor = db.query(models.Flavor).get(flavor_id)
    if not flavor:
        raise HTTPException(status_code=404, detail="Sabor não encontrado")
    flavor.active = item.active
    db.commit()
    return {"message": "Status atualizado"}