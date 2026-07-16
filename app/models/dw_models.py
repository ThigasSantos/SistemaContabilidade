from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database.dw_conexao import BaseDW

class DimMaterial(BaseDW):
    __tablename__ = 'dim_material'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), unique=True, nullable=False)

    # Relacionamento com a Fato
    fatos = relationship("FatoCusto", back_populates="material")

class DimTempo(BaseDW):
    __tablename__ = 'dim_tempo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_completa = Column(Date, unique=True, nullable=False)
    dia = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    trimestre = Column(Integer, nullable=False)

    # Relacionamento com a Fato
    fatos = relationship("FatoCusto", back_populates="tempo")

class FatoCusto(BaseDW):
    __tablename__ = 'fato_custos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Chaves Estrangeiras (Ligando a Fato às Dimensões)
    material_id = Column(Integer, ForeignKey('dim_material.id'), nullable=False)
    tempo_id = Column(Integer, ForeignKey('dim_tempo.id'), nullable=False)
    
    # O ID original da produção (útil caso precisemos atualizar ou deletar no DW)
    registro_producao_id = Column(Integer, unique=True, nullable=False)
    
    # Métricas (O que vamos somar e analisar)
    metros_utilizados = Column(Float, nullable=False)
    despesa_material = Column(Float, nullable=False)
    valor_lucro = Column(Float, nullable=False)
    preco_final = Column(Float, nullable=False)

    # Relacionamentos
    material = relationship("DimMaterial", back_populates="fatos")
    tempo = relationship("DimTempo", back_populates="fatos")