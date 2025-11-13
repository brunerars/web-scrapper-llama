# 🤖 Web Scrapper Llama: RAG com Streamlit e Groq

Este projeto é uma aplicação web interativa construída com **Streamlit** que combina funcionalidades de **Web Scraping** e **Geração Aumentada por Recuperação (RAG)**. O objetivo é permitir a criação de "coleções" de documentos a partir de URLs e, em seguida, interagir com esse conteúdo via chat, utilizando um Large Language Model (LLM) através da API Groq.

O projeto é modular e focado em facilitar a expansão e manutenção por desenvolvedores.

## ⚙️ Tecnologias Chave

A base do projeto é construída sobre um *stack* moderno de Python, focado em desenvolvimento rápido e capacidades de IA.

| Categoria | Tecnologia | Propósito |
| :--- | :--- | :--- |
| **Frontend/App** | `Streamlit` | Criação da interface web interativa e do fluxo da aplicação. |
| **Core LLM** | `Groq` (via `langchain-groq`) | Provedor de LLM de alta velocidade para as interações de Chat (RAG). |
| **Framework de IA** | `LangChain` | Orquestração do fluxo RAG, manipulação de documentos e gerenciamento de *chains*. |
| **Web Scraping** | `Firecrawl` | Serviço de scraping para extrair conteúdo limpo de URLs. |
| **Armazenamento Vetorial** | `FAISS` | Banco de dados vetorial local para indexação e recuperação rápida dos documentos. |
| **Gerenciamento de Ambiente** | `python-dotenv` | Carregamento de variáveis de ambiente (como chaves de API) a partir do arquivo `.env`. |

## 📂 Estrutura do Projeto

A organização do código segue uma separação clara de responsabilidades:

```
web-scrapper-llama/
├── app.py                  # Ponto de entrada principal da aplicação Streamlit.
├── requirements.txt        # Lista de todas as dependências do projeto.
├── .env.example            # Exemplo de arquivo de configuração de variáveis de ambiente.
├── data/                   # Diretório para armazenamento das coleções de documentos.
│   └── collections/        # Coleções de documentos indexados.
│       └── Agno/           # Exemplo de uma coleção.
│           ├── faiss_index/  # Arquivos de índice vetorial FAISS.
│           └── page_*.md     # Documentos de origem (páginas web raspadas).
├── presentation/           # Módulos de lógica de apresentação (Streamlit UI).
│   ├── chat.py             # Lógica de interface e interação do modo Chat.
│   └── scrapping.py        # Lógica de interface e interação do modo Scrapping.
└── service/                # Módulos de lógica de negócio e serviços.
    ├── rag.py              # Implementação do fluxo RAG (indexação e consulta).
    └── scrapping.py        # Lógica de serviço para a chamada do Firecrawl.
```

## 🚀 Primeiros Passos

Siga estas etapas para configurar e executar o projeto localmente.

### 1. Pré-requisitos

*   **Python 3.10+**
*   **Chave de API Groq:** Necessária para o funcionamento do LLM.
*   **Chave de API Firecrawl:** Necessária para a funcionalidade de Web Scraping.

### 2. Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/brunerars/web-scrapper-llama.git
    cd web-scrapper-llama
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    # venv\Scripts\activate   # No Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto, baseado no `.env.example`, e preencha com suas chaves de API.

    **.env**
    ```
    GROQ_API_KEY="SUA_CHAVE_GROQ_AQUI"
    FIRECRAWL_API_KEY="SUA_CHAVE_FIRECRAWL_AQUI"
    ```

### 3. Execução da Aplicação

Inicie a aplicação Streamlit a partir do diretório raiz do projeto:

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador padrão (geralmente em `http://localhost:8501`).

## 🛠️ Fluxo de Trabalho

O projeto opera em dois modos principais, selecionáveis na barra lateral:

### Modo Scrapping

1.  O usuário insere uma URL e um nome para a nova **Coleção**.
2.  O serviço `service/scrapping.py` utiliza a API **Firecrawl** para raspar o conteúdo da URL.
3.  O conteúdo raspado é processado e dividido em documentos.
4.  O serviço `service/rag.py` cria um índice vetorial **FAISS** a partir desses documentos e o armazena em `data/collections/{NomeDaColecao}/`.

### Modo Chat (RAG)

1.  O usuário seleciona uma **Coleção** existente na barra lateral.
2.  O índice FAISS da coleção é carregado.
3.  O usuário faz uma pergunta.
4.  O módulo `presentation/chat.py` utiliza o fluxo **LangChain RAG** para:
    a.  Buscar os documentos mais relevantes no índice FAISS.
    b.  Passar a pergunta do usuário e os documentos recuperados como contexto para o LLM (Groq).
    c.  O LLM gera uma resposta baseada no contexto fornecido.

## 🤝 Contribuição

Sinta-se à vontade para clonar, bifurcar e contribuir para este projeto. As principais áreas de desenvolvimento incluem:

*   **Melhoria da UI/UX:** Refinamento da interface Streamlit.
*   **Novos Serviços de Scraping:** Integração com outras ferramentas de extração de dados.
*   **Otimização do RAG:** Experimentação com diferentes *chunking strategies* e modelos de *embedding*.
*   **Persistência de Coleções:** Implementação de um banco de dados mais robusto para metadados das coleções.

Para contribuir, siga o fluxo padrão de **Git**: crie uma *branch* para sua *feature* ou correção e abra um *Pull Request* para a *branch* principal.
