import customtkinter as ctk
import re
from CTkMessagebox import CTkMessagebox
from app.controllers.precificacao_controller import PrecificacaoController

class MainView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        
        # Variáveis de Estado
        self.itens_carrinho = []
        self.id_edicao = None 
        
        self.titulo = ctk.CTkLabel(self, text="Calculadora de Precificação", font=ctk.CTkFont(size=24, weight="bold"))
        self.titulo.pack(pady=(10, 20), anchor="w", padx=20)

        # ==================== ADIÇÃO DE ITENS (Formulário Horizontal) ====================
        self.add_frame = ctk.CTkFrame(self)
        self.add_frame.pack(fill="x", padx=20, pady=5)

        # Variáveis
        self.var_material = ctk.StringVar()
        self.var_preco_kg = ctk.StringVar()
        self.var_peso_metro = ctk.StringVar()
        self.var_metros = ctk.StringVar()
        self.var_margem = ctk.StringVar()

        # --- NOVO: Comando de Validação ---
        # Registra a função no sistema de janelas para vigiar as teclas digitadas (%P = texto que está sendo inserido)
        validacao_float = (self.register(self.validar_entrada_float), '%P')

        # Coluna 0: Material (Não usa validação porque aceita letras)
        self.lbl_material = ctk.CTkLabel(self.add_frame, text="Nome do Material:")
        self.lbl_material.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")
        self.entry_material = ctk.CTkEntry(self.add_frame, width=180, textvariable=self.var_material)
        self.entry_material.grid(row=1, column=0, padx=5, pady=(0, 10))

        # Coluna 1: Preço KG (Com Validação)
        self.lbl_preco = ctk.CTkLabel(self.add_frame, text="Preço/Kg (R$):")
        self.lbl_preco.grid(row=0, column=1, padx=5, pady=(5, 0), sticky="w")
        self.entry_preco = ctk.CTkEntry(self.add_frame, width=90, textvariable=self.var_preco_kg, validate="key", validatecommand=validacao_float)
        self.entry_preco.grid(row=1, column=1, padx=5, pady=(0, 10))

        # Coluna 2: Peso Metro (Com Validação)
        self.lbl_peso = ctk.CTkLabel(self.add_frame, text="Peso/Metro (Kg):")
        self.lbl_peso.grid(row=0, column=2, padx=5, pady=(5, 0), sticky="w")
        self.entry_peso = ctk.CTkEntry(self.add_frame, width=100, textvariable=self.var_peso_metro, validate="key", validatecommand=validacao_float)
        self.entry_peso.grid(row=1, column=2, padx=5, pady=(0, 10))

        # Coluna 3: Metros (Com Validação)
        self.lbl_metros = ctk.CTkLabel(self.add_frame, text="Metros:")
        self.lbl_metros.grid(row=0, column=3, padx=5, pady=(5, 0), sticky="w")
        self.entry_metros = ctk.CTkEntry(self.add_frame, width=80, textvariable=self.var_metros, validate="key", validatecommand=validacao_float)
        self.entry_metros.grid(row=1, column=3, padx=5, pady=(0, 10))

        # Coluna 4: Margem (Com Validação)
        self.lbl_margem = ctk.CTkLabel(self.add_frame, text="Lucro (%):")
        self.lbl_margem.grid(row=0, column=4, padx=5, pady=(5, 0), sticky="w")
        self.entry_margem = ctk.CTkEntry(self.add_frame, width=80, textvariable=self.var_margem, validate="key", validatecommand=validacao_float)
        self.entry_margem.grid(row=1, column=4, padx=5, pady=(0, 10))

        # Coluna 5: Botões de Ação
        self.btn_add_item = ctk.CTkButton(self.add_frame, text="Adicionar", width=100, command=self.processar_item)
        self.btn_add_item.grid(row=1, column=5, padx=15, pady=(0, 10))

        self.btn_cancelar = ctk.CTkButton(self.add_frame, text="Cancelar", width=80, fg_color="gray", hover_color="#4b4b4b", command=self.cancelar_edicao)
        self.btn_cancelar.grid(row=1, column=6, padx=5, pady=(0, 10))
        self.btn_cancelar.grid_remove() # Inicia escondido (só aparece na edição)

        # ==================== RODAPÉ (Totais e Salvar) ====================
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(side="bottom", fill="x", padx=20, pady=10)

        self.lbl_total = ctk.CTkLabel(self.footer_frame, text="Mat: R$ 0,00   |   Lucro: R$ 0,00   |   Total Geral: R$ 0,00", font=ctk.CTkFont(size=18, weight="bold"), text_color="#10B981")
        self.lbl_total.pack(side="left", anchor="w")

        self.btn_salvar = ctk.CTkButton(self.footer_frame, text="Salvar Todos no Banco", fg_color="#2563EB", hover_color="#1d4ed8", font=ctk.CTkFont(weight="bold"), command=self.salvar_dados)
        self.btn_salvar.pack(side="right", anchor="e")

        # ==================== LISTA DE ITENS (CARRINHO) ====================
        self.carrinho_frame = ctk.CTkScrollableFrame(self, label_text="Simulações Pendentes")
        self.carrinho_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ==================== REGRAS E FUNÇÕES ====================

    def validar_entrada_float(self, valor_digitado):
        """Regra do Tkinter: Permite apenas números e no máximo um separador decimal."""
        if valor_digitado == "": # Permite apagar tudo
            return True
        
        # Regex (Expressão Regular): Verifica se a string tem números, 
        # opcionalmente seguidos de UM ponto ou UMA vírgula e mais números.
        if re.fullmatch(r"[0-9]*[.,]?[0-9]*", valor_digitado):
            return True
            
        # Se tentar digitar letras, duas vírgulas ou símbolos, a tela recusa a digitação
        return False

    def processar_item(self):
        """Coleta, faz a matemática e decide se vai pra lista ou se atualiza o banco (edição)."""
        try:
            nome = self.var_material.get().strip()
            if not nome:
                raise ValueError("O nome do material é obrigatório.")
                
            # Tratamento caso o usuário clique no botão deixando os campos vazios
            str_preco = self.var_preco_kg.get().replace(',', '.') or "0"
            str_peso = self.var_peso_metro.get().replace(',', '.') or "0"
            str_metros = self.var_metros.get().replace(',', '.') or "0"
            str_margem = self.var_margem.get().replace(',', '.') or "0"
            
            preco_kg = float(str_preco)
            peso_metro = float(str_peso)
            metros = float(str_metros)
            margem = float(str_margem)
            
            if preco_kg < 0 or peso_metro <= 0 or metros <= 0 or margem < 0:
                raise ValueError("Valores não podem ser negativos ou zerados.")

            # Chama o Controller para fazer as contas
            resultados = PrecificacaoController.simular_calculo(preco_kg, peso_metro, metros, margem)

            dados_empacotados = {
                "nome_material": nome,
                "preco_kg": preco_kg,
                "peso_por_metro": peso_metro,
                "metros_utilizados": metros,
                "margem_lucro": margem,
                "despesa_material": resultados["despesa_material"],
                "valor_lucro": resultados["valor_lucro"],
                "preco_final": resultados["preco_final"]
            }

            if self.id_edicao:
                # MODO EDIÇÃO: Atualiza direto no banco
                PrecificacaoController.atualizar_precificacao(self.id_edicao, dados_empacotados)
                CTkMessagebox(title="Sucesso", message="Registro atualizado com sucesso no banco!", icon="check")
                self.cancelar_edicao()
            else:
                # MODO NOVO: Joga pra lista (carrinho)
                self.itens_carrinho.append(dados_empacotados)
                self.atualizar_interface_carrinho()
                self._limpar_campos()

        except ValueError as e:
            msg = str(e) if "obrigatório" in str(e) else "Verifique se os valores digitados são válidos."
            CTkMessagebox(title="Erro de Preenchimento", message=msg, icon="warning")

    def atualizar_interface_carrinho(self):
        """Redesenha a lista de itens e atualiza os totais no rodapé."""
        for widget in self.carrinho_frame.winfo_children():
            widget.destroy()

        total_despesa = 0.0
        total_lucro = 0.0
        total_final = 0.0

        for index, item in enumerate(self.itens_carrinho):
            linha = ctk.CTkFrame(self.carrinho_frame)
            linha.pack(fill="x", pady=2)
            
            # Texto descritivo do item
            texto = (f"{item['metros_utilizados']}m de {item['nome_material']} | "
                     f"Custo: R$ {item['despesa_material']:.2f} | "
                     f"Lucro ({item['margem_lucro']}%): R$ {item['valor_lucro']:.2f} | "
                     f"Preço Sugerido: R$ {item['preco_final']:.2f}").replace(".", ",")
            
            ctk.CTkLabel(linha, text=texto, font=("Helvetica", 14)).pack(side="left", padx=10, pady=5)
            
            # Botão de remover
            ctk.CTkButton(linha, text="X", width=30, fg_color="#ef4444", hover_color="#b91c1c", 
                          command=lambda i=index: self.remover_item(i)).pack(side="right", padx=10, pady=5)

            total_despesa += item['despesa_material']
            total_lucro += item['valor_lucro']
            total_final += item['preco_final']

        # Atualiza a Label do Rodapé
        texto_rodape = f"Mat: R$ {total_despesa:.2f}   |   Lucro: R$ {total_lucro:.2f}   |   Total Geral: R$ {total_final:.2f}".replace(".", ",")
        self.lbl_total.configure(text=texto_rodape)
        
        # Habilita ou desabilita o botão de salvar conforme a lista
        if self.itens_carrinho:
            self.btn_salvar.configure(state="normal")
        else:
            self.btn_salvar.configure(state="disabled")

    def remover_item(self, index):
        self.itens_carrinho.pop(index)
        self.atualizar_interface_carrinho()

    def salvar_dados(self):
        """Salva todos os itens da lista no banco de dados de produção."""
        if not self.itens_carrinho:
            return

        try:
            # Salva um por um (cada um vira uma linha na tabela)
            for item in self.itens_carrinho:
                PrecificacaoController.salvar_precificacao(item)

            CTkMessagebox(title="Sucesso", message="Cálculos salvos no banco de dados!", icon="check")
            
            self.itens_carrinho.clear()
            self.atualizar_interface_carrinho()
            
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Erro ao salvar: {e}", icon="cancel")

    # ==================== CONTROLES DE EDIÇÃO E LIMPEZA ====================

    def carregar_para_edicao(self, id_registro):
        """Recebe o ID do histórico, trava a tela em modo de atualização."""
        registro = PrecificacaoController.buscar_por_id(id_registro)
        if registro:
            self.id_edicao = registro.id
            
            # Preenche os campos
            self.var_material.set(registro.nome_material)
            self.var_preco_kg.set(str(registro.preco_kg).replace('.', ','))
            self.var_peso_metro.set(str(registro.peso_por_metro).replace('.', ','))
            self.var_metros.set(str(registro.metros_utilizados).replace('.', ','))
            self.var_margem.set(str(registro.margem_lucro).replace('.', ','))
            
            # Transforma a interface para "Modo Edição"
            self.btn_add_item.configure(text="Atualizar", fg_color="#F59E0B", hover_color="#D97706")
            self.btn_cancelar.grid() 
            self.btn_salvar.configure(state="disabled")
            self.carrinho_frame.configure(label_text="Editando Registro Antigo...")

    def cancelar_edicao(self):
        """Sai do modo de edição e limpa os campos."""
        self.id_edicao = None
        self._limpar_campos()
        
        # Volta a interface ao normal
        self.btn_add_item.configure(text="Adicionar", fg_color=["#3a7ebf", "#1f538d"], hover_color=["#325882", "#14375e"])
        self.btn_cancelar.grid_remove()
        self.carrinho_frame.configure(label_text="Simulações Pendentes")
        self.atualizar_interface_carrinho() # Restaura o botão de salvar conforme o carrinho

    def _limpar_campos(self):
        self.var_material.set("")
        self.var_preco_kg.set("")
        self.var_peso_metro.set("")
        self.var_metros.set("")
        self.var_margem.set("")