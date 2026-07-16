import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.utils.paths import obter_pasta_dados

# Cria um arquivo SEPARADO apenas para as análises
CAMINHO_DW = os.path.join(obter_pasta_dados(), "dw_analitico.db")
ENGINE_DW_URL = f"sqlite:///{CAMINHO_DW}"

engine_dw = create_engine(ENGINE_DW_URL, connect_args={"check_same_thread": False})
SessionDW = sessionmaker(autocommit=False, autoflush=False, bind=engine_dw)
BaseDW = declarative_base()

def obter_sessao_dw():
    sessao = SessionDW()
    try:
        yield sessao
    finally:
        sessao.close()