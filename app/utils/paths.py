import os
import sys

def obter_caminho_recurso(caminho_relativo):
    """Garante que as imagens da pasta assets sejam encontradas no .exe"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, caminho_relativo)

def obter_pasta_dados():
    """Garante que a pasta data nasça na raiz do projeto ou ao lado do .exe."""
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(".")
        
    pasta_data = os.path.join(base_dir, "data")
    os.makedirs(pasta_data, exist_ok=True)
    return pasta_data