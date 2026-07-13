from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database.conexao import Base

class Precificacao(Base):
    __tablename__ = "calculos_precificacao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Entradas do Usuário
    nome_material = Column(String(100), nullable=False)
    preco_kg = Column(Float, nullable=False)
    peso_por_metro = Column(Float, nullable=False)
    metros_utilizados = Column(Float, nullable=False)
    margem_lucro = Column(Float, nullable=False) # Em porcentagem (ex: 30)
    
    # Valores Calculados (Salvamos no banco para não ter que recalcular no DW)
    despesa_material = Column(Float, nullable=False)
    valor_lucro = Column(Float, nullable=False)
    preco_final = Column(Float, nullable=False)
    
    data_registro = Column(DateTime, default=datetime.now)