import customtkinter as ctk
from app.database.conexao import engine, Base
from app.ui.main_window import MainWindow

def inicializar_banco():
    """Gera as tabelas nos bancos de Produção e no DW."""
    # 1. Banco de Produção
    from app.database.conexao import engine, Base
    from app.models.precificacao import Precificacao 
    Base.metadata.create_all(bind=engine)
    
    # 2. Banco do Data Warehouse (DW)
    from app.database.dw_conexao import engine_dw, BaseDW
    from app.models.dw_models import DimMaterial, DimTempo, FatoCusto
    BaseDW.metadata.create_all(bind=engine_dw)
    
    print("Bancos de dados inicializados com sucesso!")

def main():
    # 1. Cria o banco de dados
    inicializar_banco()

    # 2. Configura o tema do sistema
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # 3. Chama a Janela Principal com o Menu
    app = MainWindow()

    # 4. Inicia o programa
    app.mainloop()

if __name__ == "__main__":
    main()