import os
from typing import List, Dict, Any
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableMap
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage


class AdvancedRAGService:
    """
    Serviço RAG avançado especializado em documentação técnica.

    Features:
    - Memória conversacional para troubleshooting iterativo
    - Citações com fontes (arquivo:linha)
    - Prompt otimizado para documentação técnica
    - Code-aware chunking
    - Retrieval com mais contexto (k=7)
    """

    def __init__(self):
        # Embeddings model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

        # LLM - usando Groq para respostas rápidas
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0.1,  # Baixa temperatura para respostas mais precisas
            streaming=True    # Habilitar streaming
        )

        # Text splitter otimizado para código
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,        # Chunks maiores para preservar contexto de código
            chunk_overlap=300,      # Overlap maior para não quebrar exemplos
            separators=[
                "\n\n\n",           # Separações grandes (entre seções)
                "\n\n",             # Parágrafos
                "\n```\n",          # Fim de blocos de código
                "\n```",
                "\n##",             # Headers markdown
                "\n#",
                "\n",
                " ",
                ""
            ],
            length_function=len,
        )

        # Vector store e chain
        self.vectorstore = None
        self.chain = None
        self.retriever = None

        # Memória conversacional
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            output_key="answer",
            max_token_limit=2000  # Limitar memória para não explodir o contexto
        )

        # Armazenar metadados dos documentos
        self.doc_metadata = {}

    def load_collection(self, collection_name: str) -> bool:
        """
        Carrega uma coleção de documentos com caching FAISS.

        Args:
            collection_name: Nome da coleção a carregar

        Returns:
            bool: True se carregou com sucesso, False caso contrário
        """
        collection_path = f"data/collections/{collection_name}"
        faiss_index_path = os.path.join(collection_path, "faiss_index")

        # Verificar se índice FAISS existe
        if os.path.exists(faiss_index_path):
            print(f"✅ Carregando índice FAISS existente de: {faiss_index_path}")
            self.vectorstore = FAISS.load_local(
                faiss_index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            print(f"⚠️ Criando novo índice FAISS para '{collection_name}'...")

            # Carregar documentos
            loader = DirectoryLoader(
                collection_path,
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs={"encoding": "utf-8"},
            )
            documents = loader.load()

            if not documents:
                print("❌ Nenhum documento encontrado!")
                return False

            print(f"📄 {len(documents)} documentos encontrados")

            # Split em chunks
            texts = self.text_splitter.split_documents(documents)
            print(f"✂️ {len(texts)} chunks criados")

            # Criar vectorstore
            self.vectorstore = FAISS.from_documents(texts, self.embeddings)

            # Salvar índice
            print(f"💾 Salvando índice FAISS em: {faiss_index_path}")
            self.vectorstore.save_local(faiss_index_path)

        # Configurar retriever com mais documentos
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",  # Maximum Marginal Relevance - mais diversidade
            search_kwargs={
                "k": 7,           # Recuperar 7 documentos
                "fetch_k": 20,    # Buscar 20 e filtrar para 7 melhores
                "lambda_mult": 0.7  # Balance entre relevância e diversidade
            }
        )

        # Criar chain com memória
        self._create_chain()

        return True

    def _create_chain(self):
        """Cria a chain RAG com memória conversacional."""

        # Prompt especializado para documentação técnica
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um assistente especializado em documentação técnica para desenvolvedores.

Seu objetivo é ajudar programadores a entender e usar a documentação de forma eficiente.

DIRETRIZES:
1. **Precisão Técnica**: Seja exato e específico. Desenvolvedores precisam de detalhes.
2. **Exemplos de Código**: Sempre que possível, inclua exemplos práticos de código.
3. **Citações**: Ao referenciar informações, mencione de qual documento veio.
4. **Formatação**: Use markdown para formatar código com syntax highlighting:
   - Use ```python, ```javascript, ```bash, etc.
   - Use `código inline` para nomes de funções, variáveis, etc.
5. **Contexto Conversacional**: Use o histórico da conversa para dar respostas contextuais.
6. **Honestidade**: Se algo não está na documentação, diga claramente "não encontrei isso na documentação fornecida".

RESPONDA BASEADO NO CONTEXTO DOS DOCUMENTOS ABAIXO:

{context}

Se a pergunta envolver conceitos da conversa anterior, use o histórico para dar uma resposta mais completa."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])

        # Função para formatar documentos recuperados com fontes
        def format_docs_with_sources(docs):
            formatted = []
            sources = []

            for i, doc in enumerate(docs, 1):
                # Extrair nome do arquivo da metadata
                source = doc.metadata.get('source', 'unknown')
                file_name = os.path.basename(source)

                # Formatar documento com fonte
                formatted.append(f"[Documento {i} - {file_name}]\n{doc.page_content}\n")
                sources.append(f"- {file_name}")

            # Adicionar lista de fontes no final
            formatted.append(f"\n📚 Fontes consultadas:\n" + "\n".join(set(sources)))

            return "\n".join(formatted)

        # Função para converter histórico
        def get_chat_history():
            history = self.memory.load_memory_variables({})
            return history.get("chat_history", [])

        # Criar chain com memória
        self.chain = (
            RunnableMap({
                "context": self.retriever | format_docs_with_sources,
                "question": RunnablePassthrough(),
                "chat_history": lambda x: get_chat_history(),
            })
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def ask_question(self, question: str) -> str:
        """
        Faz uma pergunta ao sistema RAG.

        Args:
            question: Pergunta do usuário

        Returns:
            str: Resposta gerada
        """
        if not self.chain:
            return "❌ Coleção não carregada. Por favor, carregue uma coleção primeiro."

        try:
            # Invocar chain
            response = self.chain.invoke(question)

            # Salvar na memória
            self.memory.save_context(
                {"input": question},
                {"answer": response}
            )

            return response

        except Exception as e:
            print(f"❌ Erro ao processar pergunta: {e}")
            return f"❌ Erro ao processar sua pergunta: {str(e)}"

    def ask_question_stream(self, question: str):
        """
        Faz uma pergunta com streaming de resposta.

        Args:
            question: Pergunta do usuário

        Yields:
            str: Chunks da resposta sendo gerada
        """
        if not self.chain:
            yield "❌ Coleção não carregada. Por favor, carregue uma coleção primeiro."
            return

        try:
            full_response = ""

            # Stream a resposta
            for chunk in self.chain.stream(question):
                full_response += chunk
                yield chunk

            # Salvar na memória após completar
            self.memory.save_context(
                {"input": question},
                {"answer": full_response}
            )

        except Exception as e:
            print(f"❌ Erro ao processar pergunta: {e}")
            yield f"\n\n❌ Erro ao processar sua pergunta: {str(e)}"

    def get_relevant_docs(self, question: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Retorna documentos relevantes para uma pergunta.

        Args:
            question: Pergunta do usuário
            k: Número de documentos a retornar

        Returns:
            Lista de documentos com metadata
        """
        if not self.retriever:
            return []

        try:
            docs = self.retriever.get_relevant_documents(question)[:k]

            results = []
            for doc in docs:
                results.append({
                    "content": doc.page_content,
                    "source": os.path.basename(doc.metadata.get('source', 'unknown')),
                    "metadata": doc.metadata
                })

            return results

        except Exception as e:
            print(f"❌ Erro ao buscar documentos: {e}")
            return []

    def clear_memory(self):
        """Limpa a memória conversacional."""
        self.memory.clear()
        print("🧹 Memória conversacional limpa!")

    def get_memory_summary(self) -> str:
        """Retorna um resumo da memória conversacional."""
        history = self.memory.load_memory_variables({})
        messages = history.get("chat_history", [])

        if not messages:
            return "📭 Nenhuma conversa no histórico."

        summary = f"💬 Histórico: {len(messages)//2} perguntas e respostas\n\n"

        # Mostrar últimas 3 interações
        recent = messages[-6:] if len(messages) > 6 else messages

        for msg in recent:
            if isinstance(msg, HumanMessage):
                summary += f"👤 **Você**: {msg.content[:100]}...\n"
            elif isinstance(msg, AIMessage):
                summary += f"🤖 **Assistente**: {msg.content[:100]}...\n\n"

        return summary
