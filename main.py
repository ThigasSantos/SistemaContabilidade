import customtkinter as ctk
from app.database.conexao import engine, Base
from app.ui.main_window import MainWindow

def inicializar_banco():
    """Gera as tabelas no banco SQLite local."""
    from app.models.precificacao import Precificacao 
    Base.metadata.create_all(bind=engine)
    print("Banco de dados inicializado com sucesso!")

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