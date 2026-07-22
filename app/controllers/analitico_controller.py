from datetime import datetime, timedelta
from sqlalchemy import func, desc
from app.database.dw_conexao import obter_sessao_dw
from app.models.dw_models import FatoCusto, DimTempo, DimMaterial

class AnaliticoController:
    
    @staticmethod
    def _aplicar_filtro_tempo(query, filtro):
        """Aplica os filtros de data na query baseada na Dimensão Tempo."""
        hoje = datetime.now().date()
        
        if filtro == "semana":
            data_limite = hoje - timedelta(days=7)
            query = query.filter(DimTempo.data_completa >= data_limite)
        elif filtro == "mes":
            data_limite = hoje - timedelta(days=30)
            query = query.filter(DimTempo.data_completa >= data_limite)
        elif filtro == "ano":
            data_limite = hoje - timedelta(days=365)
            query = query.filter(DimTempo.data_completa >= data_limite)
        elif filtro == "3 anos":
            data_limite = hoje - timedelta(days=365*3)
            query = query.filter(DimTempo.data_completa >= data_limite)
            
        # Se for "tudo", não aplica filtro
        return query

    @staticmethod
    def obter_kpis_financeiros(filtro="mes"):
        sessao = next(obter_sessao_dw())
        try:
            # Junta a Fato com a Dimensão Tempo para poder filtrar
            q = sessao.query(
                func.sum(FatoCusto.preco_final).label('faturamento'),
                func.sum(FatoCusto.despesa_material).label('custo'),
                func.sum(FatoCusto.valor_lucro).label('lucro'),
                func.sum(FatoCusto.metros_utilizados).label('metros'),
                func.count(FatoCusto.id).label('qtd_vendas')
            ).join(DimTempo, FatoCusto.tempo_id == DimTempo.id)

            q = AnaliticoController._aplicar_filtro_tempo(q, filtro)
            resultado = q.first()

            faturamento = resultado.faturamento or 0.0
            custo = resultado.custo or 0.0
            lucro = resultado.lucro or 0.0
            metros = resultado.metros or 0.0
            qtd = resultado.qtd_vendas or 0

            ticket = (faturamento / qtd) if qtd > 0 else 0.0
            margem = (lucro / faturamento * 100) if faturamento > 0 else 0.0

            return {
                "faturamento": faturamento,
                "custo": custo,
                "lucro": lucro,
                "metros_total": metros,
                "ticket_medio": ticket,
                "margem_lucro": margem
            }
        finally:
            sessao.close()

    @staticmethod
    def obter_evolucao_faturamento(filtro="mes"):
        sessao = next(obter_sessao_dw())
        try:
            q = sessao.query(
                DimTempo.data_completa,
                func.sum(FatoCusto.preco_final).label('faturamento'),
                func.sum(FatoCusto.valor_lucro).label('lucro')
            ).join(DimTempo, FatoCusto.tempo_id == DimTempo.id)

            q = AnaliticoController._aplicar_filtro_tempo(q, filtro)
            
            # Agrupa por dia e ordena do mais antigo para o mais novo
            resultados = q.group_by(DimTempo.data_completa).order_by(DimTempo.data_completa.asc()).all()

            datas = [res.data_completa.strftime("%d/%m") for res in resultados]
            faturamentos = [res.faturamento for res in resultados]
            lucros = [res.lucro for res in resultados]

            return datas, faturamentos, lucros
        finally:
            sessao.close()

    @staticmethod
    def obter_ranking_materiais_uso(filtro="mes", limite=10):
        sessao = next(obter_sessao_dw())
        try:
            q = sessao.query(
                DimMaterial.nome,
                func.sum(FatoCusto.metros_utilizados).label('total_metros')
            ).join(FatoCusto, FatoCusto.material_id == DimMaterial.id)\
             .join(DimTempo, FatoCusto.tempo_id == DimTempo.id)

            q = AnaliticoController._aplicar_filtro_tempo(q, filtro)
            
            resultados = q.group_by(DimMaterial.nome).order_by(desc('total_metros')).limit(limite).all()
            
            return [{"nome": res.nome, "valor": res.total_metros} for res in resultados]
        finally:
            sessao.close()

    @staticmethod
    def obter_ranking_materiais_lucro(filtro="mes", limite=10):
        sessao = next(obter_sessao_dw())
        try:
            q = sessao.query(
                DimMaterial.nome,
                func.sum(FatoCusto.valor_lucro).label('total_lucro')
            ).join(FatoCusto, FatoCusto.material_id == DimMaterial.id)\
             .join(DimTempo, FatoCusto.tempo_id == DimTempo.id)

            q = AnaliticoController._aplicar_filtro_tempo(q, filtro)
            
            resultados = q.group_by(DimMaterial.nome).order_by(desc('total_lucro')).limit(limite).all()
            
            return [{"nome": res.nome, "valor": res.total_lucro} for res in resultados]
        finally:
            sessao.close()