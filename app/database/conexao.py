import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.utils.paths import obter_pasta_dados

# Cria o arquivo do banco dentro da pasta data
CAMINHO_BD = os.path.join(obter_pasta_dados(), "precificacao_prod.db")
ENGINE_URL = f"sqlite:///{CAMINHO_BD}"

engine = create_engine(ENGINE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def obter_sessao():
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()