import customtkinter as ctk
from PIL import Image
from app.utils.paths import obter_caminho_recurso
from app.ui.main_view import MainView 
from app.ui.historico_view import HistoricoView
from app.ui.analitico_view import AnaliticoView

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Simples Contabilidade - Precificação")
        self.geometry("1100x600")
        self.minsize(900, 500)

        # Configura o layout principal (1 Linha, 2 Colunas: Menu Esquerdo | Conteúdo Direito)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ================= MENU LATERAL (SIDEBAR) =================
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1) # Empurra tudo pra cima

        ctk.CTkLabel(self.sidebar_frame, text="Menu", font=("Helvetica", 24, "bold")).grid(row=0, column=0, padx=20, pady=(30, 20))

        # Botões do Menu
        self.btn_inicio = ctk.CTkButton(self.sidebar_frame, text="Início", command=self.mostrar_inicio)
        self.btn_inicio.grid(row=1, column=0, padx=20, pady=10)

        self.btn_novo = ctk.CTkButton(self.sidebar_frame, text="Adicionar Novo", command=self.mostrar_novo)
        self.btn_novo.grid(row=2, column=0, padx=20, pady=10)

        self.btn_historico = ctk.CTkButton(self.sidebar_frame, text="Histórico", command=self.mostrar_historico)
        self.btn_historico.grid(row=3, column=0, padx=20, pady=10)

        self.btn_analise = ctk.CTkButton(self.sidebar_frame, text="Visão Analítica", command=self.mostrar_analise)
        self.btn_analise.grid(row=4, column=0, padx=20, pady=10)

        # ================= ÁREA DE CONTEÚDO (DIREITA) =================
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Carregando as Telas
        self.tela_inicio = self._criar_tela_inicio()
        self.tela_novo = MainView(self.content_frame) # Aqui ele "puxa" a sua tela de formulário!
        
        # --- AJUSTE: Passamos a função iniciar_edicao para o HistoricoView ---
        self.tela_historico = HistoricoView(self.content_frame, comando_editar=self.iniciar_edicao)
        
        self.tela_analise = AnaliticoView(self.content_frame)

        # Inicia mostrando a tela de Bem Vindo
        self.mostrar_inicio()

    # --- Funções de Navegação ---
    def _limpar_conteudo(self):
        """Esconde todas as telas ativas"""
        for filho in self.content_frame.winfo_children():
            filho.grid_forget()

    def mostrar_inicio(self):
        self._limpar_conteudo()
        self.tela_inicio.grid(row=0, column=0, sticky="nsew")

    def mostrar_novo(self):
        self._limpar_conteudo()
        self.tela_novo.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def mostrar_historico(self):
        self._limpar_conteudo()
        self.tela_historico.carregar_dados() # Busca dados fresquinhos no banco
        self.tela_historico.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def mostrar_analise(self):
     self._limpar_conteudo()
     self.tela_analise.carregar_metricas_tela() 
     self.tela_analise.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    # --- NOVA FUNÇÃO DE EDIÇÃO ---
    def iniciar_edicao(self, id_registro):
        """É chamada quando o usuário clica no ✏️ da tela de Histórico."""
        # 1. Pede para a tela MainView carregar os dados desse ID específico
        self.tela_novo.carregar_para_edicao(id_registro)
        
        # 2. Muda a visão para a tela de formulário
        self.mostrar_novo()

    # --- Criação das Telas Extras ---
    def _criar_tela_inicio(self):
        """Cria a tela de Bem Vindo com a Imagem."""
        frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        
        try:
            caminho_img = obter_caminho_recurso("assets/logo.png") 
            img = Image.open(caminho_img)
            img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300))
            lbl_imagem = ctk.CTkLabel(frame, image=img_ctk, text="")
            lbl_imagem.pack(pady=(80, 20))
        except FileNotFoundError:
            ctk.CTkLabel(frame, text="[Coloque sua logo em assets/logo.png]", text_color="gray").pack(pady=(80, 20))

        ctk.CTkLabel(frame, text="Bem Vindo ao Simples Contabilidade", font=("Helvetica", 28, "bold")).pack(pady=10)
        ctk.CTkLabel(frame, text="Selecione uma opção no menu lateral para começar.", font=("Helvetica", 16), text_color="gray").pack()
        
        return frame

    def _criar_tela_temporaria(self, texto):
        """Cria um aviso temporário para as telas que ainda vamos programar."""
        frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        ctk.CTkLabel(frame, text=texto, font=("Helvetica", 24, "bold")).pack(expand=True)
        return frame