from app.services.calculo_service import CalculoService
from app.database.conexao import obter_sessao

class PrecificacaoController:
    
    @staticmethod
    def simular_calculo(preco_kg, peso_metro, metros, margem):
        """Recebe os dados da UI, manda pro Service calcular e devolve o resultado."""
        # Aqui você poderia adicionar validações extras antes de calcular
        return CalculoService.simular_valores(preco_kg, peso_metro, metros, margem)

    @staticmethod
    def salvar_precificacao(dados_simulados):
        """Recebe os dados prontos da UI e gerencia a transação no banco."""
        sessao = next(obter_sessao())
        try:
            # Salva no banco de produção
            novo_registro = CalculoService.salvar_calculo(sessao, dados_simulados)
            
            # TODO: No futuro, chamaremos aqui o serviço do DW para replicar o dado
            
            return novo_registro
        except Exception as e:
            # Em caso de erro, desfaz a transação para não quebrar o banco
            sessao.rollback()
            raise e
        finally:
            # Fecha a conexão garantindo que o arquivo .db não fique travado no Windows
            sessao.close()

    @staticmethod
    def listar_historico():
        """Busca todos os cálculos salvos no banco, do mais novo para o mais velho."""
        sessao = next(obter_sessao())
        try:
            from app.models.precificacao import Precificacao
            # Faz um SELECT * na tabela ordenando pela data decrescente
            registros = sessao.query(Precificacao).order_by(Precificacao.data_registro.desc()).all()
            return registros
        finally:
            sessao.close()

    @staticmethod
    def buscar_por_id(id_registro):
        """Busca um registro específico no banco."""
        sessao = next(obter_sessao())
        try:
            from app.models.precificacao import Precificacao
            return sessao.query(Precificacao).filter(Precificacao.id == id_registro).first()
        finally:
            sessao.close()

    @staticmethod
    def atualizar_precificacao(id_registro, dados_atualizados):
        """Atualiza um registro existente."""
        sessao = next(obter_sessao())
        try:
            from app.models.precificacao import Precificacao
            registro = sessao.query(Precificacao).filter(Precificacao.id == id_registro).first()
            
            if registro:
                # Atualiza todos os campos dinamicamente
                for chave, valor in dados_atualizados.items():
                    setattr(registro, chave, valor)
                sessao.commit()
        except Exception as e:
            sessao.rollback()
            raise e
        finally:
            sessao.close()

    @staticmethod
    def excluir_precificacao(id_registro):
        """Deleta um registro do banco."""
        sessao = next(obter_sessao())
        try:
            from app.models.precificacao import Precificacao
            registro = sessao.query(Precificacao).filter(Precificacao.id == id_registro).first()
            if registro:
                sessao.delete(registro)
                sessao.commit()
        except Exception as e:
            sessao.rollback()
            raise e
        finally:
            sessao.close()