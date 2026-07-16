from datetime import datetime
from app.database.conexao import obter_sessao
from app.database.dw_conexao import obter_sessao_dw

class ETLService:
    @staticmethod
    def atualizar_data_warehouse():
        """Move e transforma os dados da Produção para o Data Warehouse (Star Schema)."""
        sessao_prod = next(obter_sessao())
        sessao_dw = next(obter_sessao_dw())

        try:
            from app.models.precificacao import Precificacao
            from app.models.dw_models import DimMaterial, DimTempo, FatoCusto

            # 1. Extrai todos os dados de produção
            registros_prod = sessao_prod.query(Precificacao).all()

            for prod in registros_prod:
                # --- Transformação 1: Dimensão Material ---
                material = sessao_dw.query(DimMaterial).filter_by(nome=prod.nome_material).first()
                if not material:
                    material = DimMaterial(nome=prod.nome_material)
                    sessao_dw.add(material)
                    sessao_dw.flush() # Salva temporariamente para gerar o ID

                # --- Transformação 2: Dimensão Tempo ---
                data_calculo = prod.data_registro.date() # Pega só a data, sem a hora
                tempo = sessao_dw.query(DimTempo).filter_by(data_completa=data_calculo).first()
                if not tempo:
                    # Descobre qual é o trimestre matematicamente
                    trimestre_calc = (data_calculo.month - 1) // 3 + 1
                    
                    tempo = DimTempo(
                        data_completa=data_calculo,
                        dia=data_calculo.day,
                        mes=data_calculo.month,
                        ano=data_calculo.year,
                        trimestre=trimestre_calc
                    )
                    sessao_dw.add(tempo)
                    sessao_dw.flush()

                # --- Carga: Tabela Fato Custos ---
                fato = sessao_dw.query(FatoCusto).filter_by(registro_producao_id=prod.id).first()
                
                if not fato:
                    # Se não existe, cria um novo
                    fato = FatoCusto(
                        material_id=material.id,
                        tempo_id=tempo.id,
                        registro_producao_id=prod.id,
                        metros_utilizados=prod.metros_utilizados,
                        despesa_material=prod.despesa_material,
                        valor_lucro=prod.valor_lucro,
                        preco_final=prod.preco_final
                    )
                    sessao_dw.add(fato)
                else:
                    # Se já existe (caso o usuário tenha editado no histórico), apenas atualiza
                    fato.material_id = material.id
                    fato.tempo_id = tempo.id
                    fato.metros_utilizados = prod.metros_utilizados
                    fato.despesa_material = prod.despesa_material
                    fato.valor_lucro = prod.valor_lucro
                    fato.preco_final = prod.preco_final

            # Comita todas as inserções e atualizações de uma vez
            sessao_dw.commit()

        except Exception as e:
            sessao_dw.rollback()
            raise e
        finally:
            sessao_prod.close()
            sessao_dw.close()