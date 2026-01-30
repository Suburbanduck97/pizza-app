import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database import SessionLocal, engine, Base
from backend.app.models import Size, Category, Flavor, Beverage

# Recria as tabelas
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 1. Categorias
cat_salgada = Category(name="Tradicional")
cat_doce = Category(name="Doce")
db.add_all([cat_salgada, cat_doce])
db.commit()

# 2. Tamanhos (Regra de Preço do Usuário)
sizes = [
    Size(name="Média (6 Fatias)", slices=6, max_flavors=3, price=32.00),
    Size(name="Grande (8 Fatias)", slices=8, max_flavors=4, price=41.00),
    Size(name="Família (12 Fatias)", slices=12, max_flavors=4, price=51.00),
]
db.add_all(sizes)

# 3. Bebidas (O "Combo" vira um item aqui)
beverages = [
    Beverage(name="Refrigerante (Adicional Promo)", price=7.00),
    Beverage(name="Coca-Cola 2L", price=12.00),
    Beverage(name="Guaraná 2L", price=10.00),
]
db.add_all(beverages)

# 4. Sabores (Extraídos da Imagem image_c58647.jpg)
flavors_data = [
    (cat_salgada, "01 Atum", "Mussarela, Atum, Cebola e Azeitonas"),
    (cat_salgada, "02 Bibi 1", "Mussarela, Atum, Catupiry e Azeitonas"),
    (cat_salgada, "03 Bibi 2", "Mussarela, Presunto, Ovos, Pimentão, Bacon, Champignon, Milho e Azeitonas"),
    (cat_salgada, "04 Bacon", "Mussarela, Bacon e Azeitonas"),
    (cat_salgada, "05 Bauru", "Mussarela, Presunto, Tomate e Azeitonas"),
    (cat_salgada, "06 Caipira", "Mussarela, Frango, Bacon, Milho, Cebola e Azeitonas"),
    (cat_salgada, "07 Lombinho", "Mussarela, Lombinho, Cebola e Azeitonas"),
    (cat_salgada, "08 Calabresa", "Mussarela, Calabresa, Cebola e Azeitonas"),
    (cat_salgada, "09 Canadense", "Mussarela, Lombinho, Catupiry e Azeitonas"),
    (cat_salgada, "10 Florença", "Mussarela, Frango, Milho, Bacon, Ovos, Cebola e Azeitonas"),
    (cat_salgada, "11 Baiana", "Mussarela, Calabresa Moída, Ovos, Pimenta Calabresa, Cebola e Azeitonas"),
    (cat_salgada, "12 Frango", "Mussarela, Frango e Azeitonas"),
    (cat_salgada, "13 Frango Catupiry", "Mussarela, Frango, Catupiry e Azeitonas"),
    (cat_salgada, "14 Alemã", "Mussarela, Presunto e Catupiry"),
    (cat_salgada, "15 Americana", "Mussarela, Presunto, Bacon, Cebola e Azeitonas"),
    (cat_salgada, "16 Apetite", "Mussarela, Presunto, Calabresa, Cebola e Azeitonas"),
    (cat_salgada, "17 Baicatu", "Mussarela, Calabresa e Catupiry"),
    (cat_salgada, "18 Brasileira", "Mussarela, Frango, Milho, Palmito e Catupiry"),
    (cat_salgada, "19 Especial", "Mussarela, Lombo, Palmito, Bacon e Cebola"),
    (cat_salgada, "20 Mista", "Mussarela, Calabresa Moída, Cebola e Azeitonas"),
    (cat_salgada, "21 Barcelona", "Mussarela, Calabresa Moída, Champignon e Bacon"),
    (cat_salgada, "22 Genova", "Atum coberto com Mussarela e Tomate"),
    (cat_salgada, "23 Marguerita", "Mussarela, Tomate, Manjericão, Parmesão Ralado e Azeitonas"),
    (cat_salgada, "24 Milão", "Atum, Palmito, Ervilha, Ovos e Cebola cobertos por Mussarela"),
    (cat_salgada, "25 Milho", "Mussarela, Milho e Azeitonas"),
    (cat_salgada, "26 Milho Especial", "Mussarela, Milho e Catupiry"),
    (cat_salgada, "27 Parma", "Lombinho, Palmito e Milho coberto por Mussarela"),
    (cat_salgada, "28 Portuguesa", "Mussarela, Presunto, Ovos, Ervilha, Bacon, Cebola e Azeitonas"),
    (cat_salgada, "29 Romana", "Lombo Fatiado, Champignon e Cebola cobertos por Mussarela e Tomate"),
    (cat_salgada, "30 Siciliana", "Presunto e Bacon cobertos por Mussarela"),
    (cat_salgada, "31 4 Queijos", "Mussarela, Catupiry, Provolone, Gorgonzola e Parmesão ralado"),
    (cat_salgada, "32 Da Hora", "Mussarela, Presunto, Palmito, Bacon, Catupiry e Azeitonas"),
    (cat_salgada, "33 Frango com Cheddar", "Mussarela, Frango, Cheddar e Azeitonas"),
    (cat_salgada, "34 Palmito Especial", "Mussarela, Palmito e Bacon"),
    (cat_salgada, "35 Da Casa", "Mussarela, Milho, Ovos, Palmito, Champignon, Bacon e Pimentão"),
    (cat_doce, "Romeu e Julieta", "Goiabada e Mussarela"),
    (cat_doce, "Brigadeiro", "Chocolate e Granulado"),
    (cat_doce, "Prestígio", "Chocolate e Coco"),
    (cat_doce, "Banana c/ Canela", "Banana, Canela e Açúcar"),
]

for cat, name, desc in flavors_data:
    db.add(Flavor(name=name, description=desc, category=cat))

db.commit()
db.close()
print("Cardápio 'Bibi Pizza' importado com sucesso!")