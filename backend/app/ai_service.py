import random
from sqlalchemy.orm import Session
from . import models

def suggest_flavors(db: Session, size_id: int):
    size = db.query(models.Size).get(size_id)
    if not size:
        return None
    
    # Buscando sabores ativos
    savory_flavors = db.query(models.Flavor).join(models.Category)\
    .filter(models.Flavor.active == True, models.Category.name != 'Doce').all()

    limit = size.max_flavors
    suggestions = []

    # gera opções de sugestão
    for _ in range(2):
        if len(savory_flavors) >= limit:
            selected = random.sample(savory_flavors, limit)
            desc_text = "Sugestão automática! Preferências pessoais podem variar."

            suggestions.append({
                "flavors": [f.name for f in selected],
                "description": f"Combinação de {', '.join([f.name for f in selected])}",
                "disclaimer": desc_text
            })
    
    return suggestions
        