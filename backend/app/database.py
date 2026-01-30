# backend/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Tenta pegar a URL do banco externo (Neon/Render)
# Se não achar, usa o arquivo local (SQLite)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Correção para URL do Render (ele começa com postgres:// mas o SQLAlchemy quer postgresql://)
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not SQLALCHEMY_DATABASE_URL:
    # Fallback para SQLite local
    SQLALCHEMY_DATABASE_URL = "sqlite:///./pizzaria.db"
    connect_args = {"check_same_thread": False} # Só para SQLite
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
else:
    # Configuração para PostgreSQL (Neon/Production)
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()