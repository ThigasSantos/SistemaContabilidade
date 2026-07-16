# Simples Contabilidade - Sistema de Precificação e BI

Um sistema desktop moderno e responsivo desenvolvido em Python para gestão, cálculo de precificação de materiais e análise de dados (Business Intelligence). Projetado com foco em usabilidade, o sistema permite simular custos, calcular margens de lucro, armazenar históricos e analisar métricas financeiras através de um Data Warehouse integrado.

---

## Funcionalidades Principais

* **🧮 Calculadora de Precificação:** Entrada rápida de dados (Material, Preço/Kg, Peso/Metro, Metros Utilizados e Margem de Lucro) com validação em tempo real bloqueando caracteres inválidos.
* **🛒 Sistema de Carrinho:** Permite realizar múltiplas simulações e visualizá-las em uma lista pendente com totalizadores dinâmicos antes de salvar em lote no banco de dados.
* **📜 Histórico e CRUD Completo:** Visualização de todos os cálculos salvos, com capacidade de exclusão e edição inteligente (que redireciona o usuário para o formulário preenchido).
* **📈 Dashboard Analítico (Business Intelligence):**
  * Sincronização de dados via **processo de ETL** (Extração, Transformação e Carga).
  * KPIs Financeiros: Receita Total, Custo de Materiais, Lucro Líquido, Metros Utilizados, Ticket Médio e Margem de Lucro Real.
  * Gráficos interativos (Evolução Financeira em linha e Divisão da Receita em rosca).
  * Rankings automáticos: Top Materiais Mais Usados e Top Materiais com Maior Lucro.
* **⚙️ Configuração Dinâmica (.env):** Personalização do nome da empresa, logotipo e dados de contato sem necessidade de alterar o código-fonte.
* **🖼️ Interface Moderna:** Tema escuro nativo com responsividade avançada e imagens de fundo com tratamento de opacidade.

---

## Arquitetura do Projeto

O sistema foi construído utilizando o padrão **MVC (Model-View-Controller)** com separação clara de responsabilidades:

```text
SimplesContabilidade/
├── app/
│   ├── controllers/      # Regras de negócio e comunicação entre UI e Banco
│   ├── database/         # Conexões com os bancos SQLite (Produção e DW)
│   ├── models/           # Mapeamento Objeto-Relacional (SQLAlchemy)
│   ├── services/         # Serviços isolados (Matemática, ETL, Configurações)
│   ├── ui/               # Telas do sistema construídas com CustomTkinter
│   └── utils/            # Ferramentas auxiliares (paths.py, config.py)
├── assets/               # Imagens estáticas (logo.png, background.png, icon.ico)
├── data/                 # Pasta autogerada contendo os bancos de dados (.db)
├── .env                  # Variáveis de ambiente (Nome da Empresa, etc.)
├── main.py               # Ponto de entrada da aplicação
└── README.md
```

## Tecnologias Utilizadas

* **Linguagem: Python 3.10+**
* **Interface Gráfica:** customtkinter **(UI Moderna)**, CTkMessagebox **(Alertas)**.
* **Manipulação de Imagem:** Pillow **(PIL)**.
* **Visualização de Dados:** matplotlib **(Gráficos no Dashboard)**.
* **Banco de Dados & ORM:** SQLAlchemy, SQLite3.
* **Data Warehouse:** Modelagem Star Schema **(Tabela Fato e Dimensões)**.
* **Variáveis de Ambiente:** python-dotenv.

## Como Instalar e Rodar

### 1. Pré-requisitos
Certifique-se de ter o Python instalado na sua máquina. É altamente recomendável utilizar um ambiente virtual (`venv`).

### 2. Clonar o repositório

```bash
git clone https://seu-repositorio-aqui.git
cd SimplesContabilidade
```

### 3. Criar e ativar o ambiente virtual

- **Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

- **Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar as dependências

```bash
pip install customtkinter Pillow SQLAlchemy matplotlib CTkMessagebox python-dotenv
```

### 5. Configurar o arquivo `.env`
Crie um arquivo chamado `.env` na raiz do projeto, no mesmo nível do `main.py`, e insira as informações da sua empresa:

```env
NOME_EMPRESA="Rede da Mata"
CNPJ="00.000.000/0001-00"
ENDERECO="Rua Principal, 123"
TELEFONE="(00) 00000-0000"
EMAIL="contato@empresa.com.br"
```

### 6. Configurar as imagens
Crie uma pasta chamada `assets` na raiz do projeto e adicione os seguintes arquivos:

- `logo.png` - logo com fundo transparente
- `background.png` - imagem de fundo/capa
- `icon.ico` - ícone do aplicativo

### 7. Rodar a aplicação

```bash
python main.py
```

## Estrutura de Banco de Dados

Para garantir que o sistema de relatórios não sobrecarregue a operação diária, o projeto utiliza dois bancos de dados SQLite isolados dentro da pasta `data/`:

1. **`producao.db`:** Banco de operação rápida. Armazena a tabela `calculos_precificacao` com os dados brutos de entrada.
2. **`dw_analitico.db`:** Data Warehouse estruturado em **Star Schema** para consultas pesadas do Dashboard.

- `fato_custos` (Tabela Central de Métricas)
- `dim_material` (Dimensão de Produto)
- `dim_tempo` (Dimensão de Data/Trimestre)

O motor de ETL (`ETLService`) faz a ponte entre esses dois bancos sob demanda.

## 📦 Como Compilar para Executável (.exe)

O sistema foi arquitetado (`paths.py`) pensando na compilação via **PyInstaller**. Para gerar o executável final:

1. Instale o PyInstaller:

```bash
pip install pyinstaller
```

2. Rode o comando de compilação:

```bash
pyinstaller --noconfirm --windowed --name "SimplesContabilidade" --icon "assets/icon.ico" --add-data "assets;assets" --add-data ".env;." main.py
```

*(Nota: Se estiver usando Linux/Mac, troque o `;` por `:` no parâmetro `--add-data`)*

3. O arquivo final estará disponível na pasta `dist/`.