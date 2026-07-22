import customtkinter as ctk
from app.controllers.precificacao_controller import PrecificacaoController

class HistoricoView(ctk.CTkFrame):
    # --- AJUSTE: Adicionamos o 'comando_editar' para conversar com a tela principal ---
    def __init__(self, master, comando_editar):
        super().__init__(master, fg_color="transparent")
        self.comando_editar = comando_editar

        # Título da Tela
        ctk.CTkLabel(self, text="Histórico de Cálculos", font=("Helvetica", 24, "bold")).pack(pady=(10, 20), anchor="w", padx=20)

        # Container com barra de rolagem (Nossa "Tabela")
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def carregar_dados(self):
        """Limpa a tabela e recarrega os dados do banco (útil para atualizar a tela)."""
        # 1. Limpa os dados antigos da tela
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # 2. Desenha os cabeçalhos das colunas (Adicionamos "Ações" no final)
        cabecalhos = ["Data", "Material", "Custo", "Lucro", "Preço Final", "Margem", "Ações"]
        for col, texto in enumerate(cabecalhos):
            lbl = ctk.CTkLabel(self.scroll_frame, text=texto, font=("Helvetica", 14, "bold"))
            lbl.grid(row=0, column=col, padx=15, pady=10, sticky="w")

        # 3. Busca os dados no banco via Controller
        registros = PrecificacaoController.listar_historico()

        if not registros:
            ctk.CTkLabel(self.scroll_frame, text="Nenhum cálculo salvo ainda.", text_color="gray").grid(row=1, column=0, columnspan=7, pady=20)
            return

        # 4. Preenche as linhas da tabela
        for row, reg in enumerate(registros, start=1):
            # Formata a data (Ex: 14/07/2026 15:30)
            data_str = reg.data_registro.strftime("%d/%m/%Y %H:%M")
            
            ctk.CTkLabel(self.scroll_frame, text=data_str).grid(row=row, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=reg.nome_material).grid(row=row, column=1, padx=15, pady=5, sticky="w")
            
            ctk.CTkLabel(self.scroll_frame, text=f"R$ {reg.despesa_material:.2f}".replace(".", ",")).grid(row=row, column=2, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=f"R$ {reg.valor_lucro:.2f}".replace(".", ","), text_color="#10B981").grid(row=row, column=3, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=f"R$ {reg.preco_final:.2f}".replace(".", ",")).grid(row=row, column=4, padx=15, pady=5, sticky="w")
            
            ctk.CTkLabel(self.scroll_frame, text=f"{reg.margem_lucro}%").grid(row=row, column=5, padx=15, pady=5, sticky="w")
            
            # --- NOVO: Botões de Ação ---
            frame_acoes = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            frame_acoes.grid(row=row, column=6, padx=10, pady=5)
            
            # Botão Editar
            btn_edit = ctk.CTkButton(frame_acoes, text="✏️", width=30, command=lambda id_reg=reg.id: self.comando_editar(id_reg))
            btn_edit.pack(side="left", padx=5)
            
            # Botão Excluir
            btn_del = ctk.CTkButton(frame_acoes, text="🗑️", width=30, fg_color="#EF4444", hover_color="#B91C1C", 
                                    command=lambda id_reg=reg.id: self._confirmar_exclusao(id_reg))
            btn_del.pack(side="left")

    # --- NOVA FUNÇÃO ---
    def _confirmar_exclusao(self, id_registro):
        """Chama o Controller para excluir o registro e recarrega a tabela visualmente."""
        try:
            PrecificacaoController.excluir_precificacao(id_registro)
            self.carregar_dados() # Recarrega a tela para a linha sumir
        except Exception as e:
            print(f"Erro ao excluir: {e}")