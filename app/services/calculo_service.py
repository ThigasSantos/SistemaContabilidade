class CalculoService:
    
    @staticmethod
    def simular_valores(preco_kg, peso_por_metro, metros_utilizados, margem_lucro_pct):
        """Faz a matemática em tempo real para a tela antes de salvar."""
        
        # 1. Descobre quantos KG foram usados no total
        kg_total_utilizado = peso_por_metro * metros_utilizados
        
        # 2. Custo da Despesa de Material
        despesa_material = kg_total_utilizado * preco_kg
        
        # 3. Lucro
        valor_lucro = despesa_material * (margem_lucro_pct / 100.0)
        
        # 4. Preço Final
        preco_final = despesa_material + valor_lucro
        
        return {
            "despesa_material": round(despesa_material, 2),
            "valor_lucro": round(valor_lucro, 2),
            "preco_final": round(preco_final, 2)
        }

    @staticmethod
    def salvar_calculo(sessao_db, dados_calculo):
        """Salva no banco de produção. (Aqui também podemos acionar a cópia pro DW depois)."""
        from app.models.precificacao import Precificacao
        
        novo_registro = Precificacao(**dados_calculo)
        sessao_db.add(novo_registro)
        sessao_db.commit()
        
        return novo_registro