import customtkinter as ctk
import os
from PIL import Image, ImageEnhance
from app.utils.paths import obter_caminho_recurso
from app.utils.config import NOME_EMPRESA
from app.ui.main_view import MainView 
from app.ui.historico_view import HistoricoView
from app.ui.analitico_view import AnaliticoView

# Configuração visual padrão do aplicativo
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela (Puxando o nome do arquivo .env)
        self.title(f"{NOME_EMPRESA} - Precificação")
        self.geometry("1280x800")
        self.minsize(1000, 700)

        # Configura o ícone da janela
        try:
            caminho_icone = obter_caminho_recurso("assets/icon.ico")
            if os.path.exists(caminho_icone):
                self.iconbitmap(caminho_icone)
        except Exception as e:
            print(f"Aviso: Não foi possível carregar o ícone. Detalhes: {e}")

        # Configuração do Grid Principal (1 Linha, 2 Colunas)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1) # A coluna 1 (área principal) vai expandir

        # ==================== SIDEBAR (Menu Lateral) ====================
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # Empurra o rodapé para o final
        self.sidebar_frame.grid_rowconfigure(6, weight=1) 

        # Logo no Topo
        caminho_logo = obter_caminho_recurso("assets/logo.png")
        if os.path.exists(caminho_logo):
            self.img_logo = ctk.CTkImage(light_image=Image.open(caminho_logo), dark_image=Image.open(caminho_logo), size=(150, 80))
            self.lbl_logo = ctk.CTkLabel(self.sidebar_frame, text="", image=self.img_logo)
            self.lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 30))
        else:
            self.lbl_logo = ctk.CTkLabel(self.sidebar_frame, text="[Logo]", font=ctk.CTkFont(size=20, weight="bold"))
            self.lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 30))

        # Botões de Navegação
        self.btn_inicio = ctk.CTkButton(self.sidebar_frame, text="🏠 Início", command=self.mostrar_inicio)
        self.btn_inicio.grid(row=1, column=0, padx=20, pady=10)

        self.btn_novo = ctk.CTkButton(self.sidebar_frame, text="➕ Novo Cálculo", command=self.mostrar_novo)
        self.btn_novo.grid(row=2, column=0, padx=20, pady=10)

        self.btn_historico = ctk.CTkButton(self.sidebar_frame, text="📜 Histórico", command=self.mostrar_historico)
        self.btn_historico.grid(row=3, column=0, padx=20, pady=10)

        self.btn_analitico = ctk.CTkButton(self.sidebar_frame, text="📊 Dashboard", command=self.mostrar_analise)
        self.btn_analitico.grid(row=4, column=0, padx=20, pady=10)

        # Rodapé da Sidebar
        self.rodape_label = ctk.CTkLabel(self.sidebar_frame, text="v1.0", text_color="gray")
        self.rodape_label.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # ==================== ÁREA PRINCIPAL ====================
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # ==================== TELAS PRÉ-CARREGADAS ====================
        # Instanciamos as telas apenas UMA vez para não perder os dados do carrinho!
        self.tela_novo = MainView(self.main_frame)
        self.tela_historico = HistoricoView(self.main_frame, comando_editar=self.iniciar_edicao)
        self.tela_analise = AnaliticoView(self.main_frame)

        # Carrega e processa a Imagem de Fundo (Capa) para a Tela Início
        caminho_capa = obter_caminho_recurso("assets/background.png")
        if os.path.exists(caminho_capa):
            imagem_original = Image.open(caminho_capa)
            escurecedor = ImageEnhance.Brightness(imagem_original)
            imagem_fosca = escurecedor.enhance(0.4) # Deixando 40% do brilho original para o tema Dark
            
            self.img_capa = ctk.CTkImage(light_image=imagem_fosca, dark_image=imagem_fosca, size=(100, 100))
            self.lbl_fundo = ctk.CTkLabel(self.main_frame, text="", image=self.img_capa)
        else:
            self.lbl_fundo = ctk.CTkLabel(self.main_frame, text=f"Bem-vindo ao {NOME_EMPRESA}", font=ctk.CTkFont(size=26, weight="bold"))

        # Inicia mostrando a tela de fundo
        self.mostrar_inicio()

    # ==================== FUNÇÕES DE NAVEGAÇÃO ====================
    
    def limpar_main_frame(self):
        """Esconde todas as telas ativas sem destruí-las, preservando os dados digitados."""
        self.main_frame.unbind("<Configure>") # Desliga o ajustador de imagem temporariamente
        
        # Remove a imagem de fundo e todas as sub-telas da visualização
        self.lbl_fundo.place_forget()
        for widget in self.main_frame.winfo_children():
            # Apenas esconde as telas. Não usa widget.destroy()!
            if widget != self.lbl_fundo:
                widget.pack_forget()

    def mostrar_inicio(self):
        self.limpar_main_frame()
        if hasattr(self, 'img_capa'):
            self.lbl_fundo.place(x=0, y=0, relwidth=1, relheight=1)
            self.main_frame.bind("<Configure>", self.redimensionar_background)
        else:
            self.lbl_fundo.place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_novo(self):
        self.limpar_main_frame()
        self.tela_novo.pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar_historico(self):
        self.limpar_main_frame()
        self.tela_historico.carregar_dados() # Busca dados fresquinhos no banco
        self.tela_historico.pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar_analise(self):
        self.limpar_main_frame()
        self.tela_analise.carregar_metricas_tela() 
        self.tela_analise.pack(fill="both", expand=True, padx=10, pady=10)

    def iniciar_edicao(self, id_registro):
        """Muda para a aba de cálculo e manda preencher os dados antigos."""
        self.mostrar_novo()
        self.tela_novo.carregar_para_edicao(id_registro)

    # ==================== RESPONSIVIDADE DE IMAGEM ====================

    def redimensionar_background(self, event):
        """Ajusta a imagem de fundo toda vez que a janela muda de tamanho."""
        if hasattr(self, 'lbl_fundo') and self.lbl_fundo.winfo_exists():
            nova_largura = event.width
            nova_altura = event.height
            
            if nova_largura > 10 and nova_altura > 10:
                self.img_capa.configure(size=(nova_largura, nova_altura))