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