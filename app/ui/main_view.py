import customtkinter as ctk
from app.services.calculo_service import CalculoService
from app.controllers.precificacao_controller import PrecificacaoController
from app.database.conexao import obter_sessao

class MainView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        
        # Configuração do Grid Principal (2 colunas: Formulário | Resultados)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= ESQUERDA: FORMULÁRIO =================
        self.frame_form = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_form.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.frame_form, text="Entrada de Dados", font=("Helvetica", 20, "bold")).pack(pady=(0, 20))

        # Variáveis
        self.var_material = ctk.StringVar()
        self.var_preco_kg = ctk.StringVar()
        self.var_peso_metro = ctk.StringVar()
        self.var_metros = ctk.StringVar()
        self.var_margem = ctk.StringVar()

        # Campos
        self._criar_campo(self.frame_form, "Nome do Material", self.var_material)
        self._criar_campo(self.frame_form, "Preço do KG (R$)", self.var_preco_kg)
        self._criar_campo(self.frame_form, "Peso por Metro (KG)", self.var_peso_metro)
        self._criar_campo(self.frame_form, "Metros Utilizados", self.var_metros)
        self._criar_campo(self.frame_form, "Margem de Lucro (%)", self.var_margem)

        # Botão de Calcular (Simulação)
        self.btn_calcular = ctk.CTkButton(self.frame_form, text="Calcular Custos", command=self.atualizar_resultados)
        self.btn_calcular.pack(pady=20, fill="x")

        # ================= DIREITA: RESULTADOS =================
        self.frame_resultados = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=15) # Cor de fundo levemente destacada
        self.frame_resultados.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.frame_resultados, text="Análise de Precificação", font=("Helvetica", 20, "bold"), text_color="white").pack(pady=(20, 30))

        # Labels de Saída
        self.lbl_despesa = ctk.CTkLabel(self.frame_resultados, text="Despesa de Material: R$ 0,00", font=("Helvetica", 16))
        self.lbl_despesa.pack(pady=10)

        self.lbl_lucro = ctk.CTkLabel(self.frame_resultados, text="Lucro Estimado: R$ 0,00", font=("Helvetica", 16), text_color="#10B981") # Verde
        self.lbl_lucro.pack(pady=10)

        self.lbl_final = ctk.CTkLabel(self.frame_resultados, text="Preço Final Sugerido: R$ 0,00", font=("Helvetica", 22, "bold"))
        self.lbl_final.pack(pady=30)

        # Dicionário temporário para segurar os dados antes de salvar
        self.dados_simulados = None

        # Botão de Salvar no Banco
        self.btn_salvar = ctk.CTkButton(self.frame_resultados, text="Salvar no Sistema", command=self.salvar_dados, fg_color="#2563EB", state="disabled")
        self.btn_salvar.pack(pady=20, fill="x", padx=40)

    def _criar_campo(self, parent, label_text, var_control):
        ctk.CTkLabel(parent, text=label_text).pack(anchor="w", padx=10)
        entry = ctk.CTkEntry(parent, textvariable=var_control, width=300)
        entry.pack(pady=(0, 10), padx=10)

    def atualizar_resultados(self):
        """Coleta os dados da tela e pede pro Controller calcular."""
        try:
            nome = self.var_material.get()
            preco_kg = float(self.var_preco_kg.get().replace(',', '.'))
            peso_metro = float(self.var_peso_metro.get().replace(',', '.'))
            metros = float(self.var_metros.get().replace(',', '.'))
            margem = float(self.var_margem.get().replace(',', '.'))

            # Chama o Controller em vez do Service diretamente
            resultados = PrecificacaoController.simular_calculo(preco_kg, peso_metro, metros, margem)

            # Atualiza os textos na tela
            self.lbl_despesa.configure(text=f"Despesa de Material: R$ {resultados['despesa_material']:.2f}".replace('.', ','))
            self.lbl_lucro.configure(text=f"Lucro Estimado: R$ {resultados['valor_lucro']:.2f}".replace('.', ','))
            self.lbl_final.configure(text=f"Preço Final Sugerido: R$ {resultados['preco_final']:.2f}".replace('.', ','))

            # Prepara o pacote para salvamento
            self.dados_simulados = {
                "nome_material": nome,
                "preco_kg": preco_kg,
                "peso_por_metro": peso_metro,
                "metros_utilizados": metros,
                "margem_lucro": margem,
                "despesa_material": resultados["despesa_material"],
                "valor_lucro": resultados["valor_lucro"],
                "preco_final": resultados["preco_final"]
            }

            self.btn_salvar.configure(state="normal")

        except ValueError:
            self.lbl_final.configure(text="Erro: Verifique se os valores são números válidos.")

    def salvar_dados(self):
        """Pede pro Controller salvar o pacote no banco."""
        if self.dados_simulados:
            try:
                # O Controller faz todo o trabalho sujo de abrir e fechar sessões
                PrecificacaoController.salvar_precificacao(self.dados_simulados)

                # Feedback visual de sucesso e trava o botão novamente
                self.lbl_final.configure(text="✔️ Salvo com Sucesso!")
                self.btn_salvar.configure(state="disabled")
                
            except Exception as e:
                self.lbl_final.configure(text=f"Erro ao salvar: {e}")