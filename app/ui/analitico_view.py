import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.services.etl_service import ETLService
from app.controllers.analitico_controller import AnaliticoController

class AnaliticoView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) 
        self.grid_rowconfigure(4, weight=1) 

        # ==================== LINHA 0: CABEÇALHO E FILTROS ====================
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.header_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.header_frame, text="Dashboard Analítico", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, sticky="w")

        self.controles_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.controles_frame.grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(self.controles_frame, text="Período:").pack(side="left", padx=10)
        
        self.var_filtro = ctk.StringVar(value="mes")
        self.combo_filtro = ctk.CTkComboBox(
            self.controles_frame, 
            values=["semana", "mes", "ano", "3 anos", "tudo"], 
            variable=self.var_filtro,
            command=self.carregar_metricas_tela,
            width=120
        )
        self.combo_filtro.pack(side="left", padx=10)

        self.btn_atualizar = ctk.CTkButton(self.controles_frame, text="🔄 Sincronizar DW", fg_color="#1f538d", hover_color="#14375e", command=self.disparar_etl)
        self.btn_atualizar.pack(side="left", padx=10)

        # ==================== LINHA 1: KPIS PRINCIPAIS ====================
        self.kpi_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        for i in range(4): self.kpi_frame.grid_columnconfigure(i, weight=1)

        self.lbl_faturamento = self.criar_card_kpi(self.kpi_frame, "Receita Total", "R$ 0.00", 0, text_color="#2ecc71")
        self.lbl_despesa = self.criar_card_kpi(self.kpi_frame, "Custo Materiais", "R$ 0.00", 1, text_color="#e74c3c")
        self.lbl_lucro = self.criar_card_kpi(self.kpi_frame, "Lucro Líquido", "R$ 0.00", 2, text_color="#3498db")
        self.lbl_metros = self.criar_card_kpi(self.kpi_frame, "Metros Utilizados", "0.0 m", 3, text_color="#f39c12")

        # ==================== LINHA 2: KPIS ESTRATÉGICOS ====================
        self.sub_kpi_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sub_kpi_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        for i in range(2): self.sub_kpi_frame.grid_columnconfigure(i, weight=1)

        self.lbl_ticket = self.criar_card_kpi(self.sub_kpi_frame, "Ticket Médio", "R$ 0.00", 0, text_color="white", subtitulo="(Valor médio gerado por cálculo)")
        self.lbl_margem = self.criar_card_kpi(self.sub_kpi_frame, "Margem de Lucro Real", "0.00%", 1, text_color="white", subtitulo="(Fatia da receita que virou lucro)")

        # ==================== LINHA 3: GRÁFICOS (Evolução e Rosca) ====================
        self.graficos_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.graficos_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=5)
        self.graficos_frame.grid_columnconfigure(0, weight=3) # Gráfico de linha ocupa 60%
        self.graficos_frame.grid_columnconfigure(1, weight=2) # Gráfico de rosca ocupa 40%
        self.graficos_frame.grid_rowconfigure(0, weight=1)

        self.grafico_linha_frame = ctk.CTkFrame(self.graficos_frame, fg_color="#2b2b2b")
        self.grafico_linha_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        self.grafico_rosca_frame = ctk.CTkFrame(self.graficos_frame, fg_color="#2b2b2b")
        self.grafico_rosca_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        self.canvas_grafico_linha = None
        self.canvas_grafico_rosca = None

        # ==================== LINHA 4: RANKINGS ====================
        self.rankings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.rankings_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=10)
        self.rankings_frame.grid_columnconfigure(0, weight=1)
        self.rankings_frame.grid_columnconfigure(1, weight=1)
        self.rankings_frame.grid_rowconfigure(0, weight=1)

        self.frame_materiais = ctk.CTkScrollableFrame(self.rankings_frame, label_text="Top Materiais (Mais Usados)", label_font=ctk.CTkFont(weight="bold"))
        self.frame_materiais.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.frame_materiais_lucro = ctk.CTkScrollableFrame(self.rankings_frame, label_text="Top Materiais (Maior Lucro)", label_font=ctk.CTkFont(weight="bold"))
        self.frame_materiais_lucro.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # A carga inicial será chamada pela MainWindow ou ao iniciar, se o banco existir.
        # self.carregar_metricas_tela()

    # ==================== FUNÇÕES AUXILIARES ====================

    def criar_card_kpi(self, master, titulo, valor_inicial, coluna, text_color="white", subtitulo=None):
        card = ctk.CTkFrame(master)
        card.grid(row=0, column=coluna, sticky="ew", padx=5)
        
        ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(size=14)).pack(pady=(10, 0))
        
        if subtitulo:
            ctk.CTkLabel(card, text=subtitulo, font=ctk.CTkFont(size=10), text_color="gray").pack(pady=(0, 0))
            
        lbl_valor = ctk.CTkLabel(card, text=valor_inicial, font=ctk.CTkFont(size=22, weight="bold"), text_color=text_color)
        lbl_valor.pack(pady=(5, 10))
        
        return lbl_valor

    def disparar_etl(self):
        self.btn_atualizar.configure(state="disabled", text="Sincronizando...")
        self.update_idletasks() 
        try:
            # Chama o serviço (que vamos criar a seguir)
            ETLService.atualizar_data_warehouse()
            self.carregar_metricas_tela()
            CTkMessagebox(title="Sucesso", message="Data Warehouse atualizado com as últimas simulações!", icon="check")
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Falha na sincronização:\n{str(e)}", icon="cancel")
        finally:
            self.btn_atualizar.configure(state="normal", text="🔄 Sincronizar DW")

    def renderizar_lista(self, frame, dados, prefixo="", sufixo=""):
        for widget in frame.winfo_children(): widget.destroy()
        if not dados:
            ctk.CTkLabel(frame, text="Nenhum dado neste período.", text_color="gray").pack(pady=20)
            return
        for indice, item in enumerate(dados):
            linha = ctk.CTkFrame(frame, fg_color="transparent")
            linha.pack(fill="x", pady=5)
            ctk.CTkLabel(linha, text=f"{indice + 1}º - {item['nome']}", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
            
            # Ajuste de formatação para exibir número de metros ou valor em R$
            valor_formatado = f"{item['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            ctk.CTkLabel(linha, text=f"{prefixo} {valor_formatado} {sufixo}".strip()).pack(side="right", padx=10)

    # ==================== MOTORES GRÁFICOS E CARGA ====================
    def carregar_metricas_tela(self, *args):
        filtro = self.var_filtro.get()
        try:
            # 1. Alimenta os 6 KPIs Visuais
            kpis = AnaliticoController.obter_kpis_financeiros(filtro)
            self.lbl_faturamento.configure(text=f"R$ {kpis['faturamento']:,.2f}".replace('.', ','))
            self.lbl_despesa.configure(text=f"R$ {kpis['custo']:,.2f}".replace('.', ','))
            self.lbl_lucro.configure(text=f"R$ {kpis['lucro']:,.2f}".replace('.', ','))
            self.lbl_metros.configure(text=f"{kpis['metros_total']:,.1f} m".replace('.', ','))
            
            self.lbl_ticket.configure(text=f"R$ {kpis['ticket_medio']:,.2f}".replace('.', ','))
            self.lbl_margem.configure(text=f"{kpis['margem_lucro']:,.1f}%".replace('.', ','))

            # 2. Renderiza Gráficos (Adaptados)
            self.renderizar_grafico_evolucao(*AnaliticoController.obter_evolucao_faturamento(filtro))
            self.renderizar_grafico_rosca(kpis['custo'], kpis['lucro'])

            # 3. Renderiza Rankings (Adaptados)
            self.renderizar_lista(self.frame_materiais, AnaliticoController.obter_ranking_materiais_uso(filtro, 10), sufixo="m")
            self.renderizar_lista(self.frame_materiais_lucro, AnaliticoController.obter_ranking_materiais_lucro(filtro, 10), prefixo="R$")
            
        except Exception as e:
            print(f"[UI ERROR] Erro ao carregar métricas (provavelmente o DW está vazio): {e}")

    def renderizar_grafico_evolucao(self, datas, faturamentos, lucros):
        if self.canvas_grafico_linha: self.canvas_grafico_linha.get_tk_widget().destroy()
        fig = Figure(figsize=(6, 3), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2b2b2b')

        if not datas:
            ax.text(0.5, 0.5, "Sem dados para o período", ha='center', va='center', color='gray')
            ax.axis('off')
        else:
            ax.plot(datas, faturamentos, marker='o', color='#2ecc71', label='Receita', linewidth=2)
            ax.plot(datas, lucros, marker='o', color='#3498db', label='Lucro', linewidth=2)
            ax.set_title("Evolução Financeira", color='white', pad=10)
            ax.legend(frameon=False, labelcolor='white')
            ax.tick_params(axis='x', colors='white', rotation=45)
            ax.tick_params(axis='y', colors='white')
            for spine in ax.spines.values(): spine.set_color('gray')
            ax.grid(True, linestyle='--', alpha=0.3)
            fig.tight_layout()

        self.canvas_grafico_linha = FigureCanvasTkAgg(fig, master=self.grafico_linha_frame)
        self.canvas_grafico_linha.draw()
        self.canvas_grafico_linha.get_tk_widget().pack(fill="both", expand=True)

    def renderizar_grafico_rosca(self, custo, lucro):
        """Gráfico de anel agora divide apenas Custo vs Lucro."""
        if self.canvas_grafico_rosca: self.canvas_grafico_rosca.get_tk_widget().destroy()

        fig = Figure(figsize=(4, 3), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')
        ax = fig.add_subplot(111)

        if custo == 0 and lucro == 0:
            ax.text(0.5, 0.5, "Sem detalhamento", ha='center', va='center', color='gray')
            ax.axis('off')
        else:
            valores = [custo, lucro]
            labels = ['Material', 'Lucro']
            cores = ['#e74c3c', '#3498db']
            
            wedges, texts, autotexts = ax.pie(
                valores, 
                colors=cores, 
                autopct='%1.1f%%', 
                startangle=90,
                pctdistance=0.75, 
                textprops=dict(color="white", fontsize=12, weight="bold"),
                wedgeprops=dict(width=0.4, edgecolor='#2b2b2b', linewidth=2)
            )
            
            ax.set_title("Divisão da Receita", color='white', pad=15)
            
            ax.legend(
                wedges, labels,
                loc="lower center", 
                bbox_to_anchor=(0.5, -0.15),
                ncol=2, 
                frameon=False, 
                labelcolor="white", 
                fontsize=10
            )
            
            fig.tight_layout()

        self.canvas_grafico_rosca = FigureCanvasTkAgg(fig, master=self.grafico_rosca_frame)
        self.canvas_grafico_rosca.draw()
        self.canvas_grafico_rosca.get_tk_widget().pack(fill="both", expand=True)