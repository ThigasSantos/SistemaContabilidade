import os
import sys
from dotenv import load_dotenv

def obter_caminho_raiz():
    """Garante que o .env seja lido na raiz, mesmo após virar .exe"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(".")

# Carrega o arquivo .env
caminho_env = os.path.join(obter_caminho_raiz(), '.env')
load_dotenv(caminho_env)

# Exporta as variáveis prontas para uso (com valores padrão caso o .env não exista)
NOME_EMPRESA = os.getenv("NOME_EMPRESA", "Simples Contabilidade")
CNPJ = os.getenv("CNPJ", "00.000.000/0000-00")
ENDERECO = os.getenv("ENDERECO", "Endereço não informado")
TELEFONE = os.getenv("TELEFONE", "Telefone não informado")
EMAIL = os.getenv("EMAIL", "E-mail não informado")