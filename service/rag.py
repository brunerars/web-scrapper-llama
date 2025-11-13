import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vectorstore = None
        self.chain = None

    def load_collection(self, collection_name):
        collection_path = f"data/collections/{collection_name}"
        # O índice FAISS será salvo dentro da própria pasta da coleção
        faiss_index_path = os.path.join(collection_path, "faiss_index")

        # --- LÓGICA DE CACHING ---
        # 1. VERIFICAR SE O ÍNDICE JÁ EXISTE
        if os.path.exists(faiss_index_path):
            print(f"✅ Carregando índice FAISS existente de: {faiss_index_path}")
            # Se existe, carrega do disco (muito rápido!)
            self.vectorstore = FAISS.load_local(faiss_index_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            print(f"⚠️ Índice FAISS não encontrado. Criando um novo para a coleção '{collection_name}'.")
            # 2. SE NÃO EXISTE, FAZ O TRABALHO PESADO
            loader = DirectoryLoader(
                collection_path,
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs={"encoding": "utf-8"},
            )
            documents = loader.load()
            if not documents:
                return False

            texts = self.text_splitter.split_documents(documents)
            
            # O processo lento que só roda uma vez por coleção
            self.vectorstore = FAISS.from_documents(texts, self.embeddings)
            
            # 3. SALVA O NOVO ÍNDICE EM DISCO PARA USO FUTURO
            print(f"💾 Salvando novo índice FAISS em: {faiss_index_path}")
            self.vectorstore.save_local(faiss_index_path)
        
        # O resto do código para criar a chain permanece o mesmo
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        prompt = ChatPromptTemplate.from_template("""
Responda baseado APENAS no contexto abaixo.
Se não houver resposta nos documentos, diga que não sabe.

CONTEXT:
{context}

QUESTION:
{question}
""")
        self.chain = (
            RunnableMap({
                "context": retriever,
                "question": lambda x: x,
            })
            | prompt
            | self.llm
            | StrOutputParser()
        )
        return True

    def ask_question(self, question):
        if not self.chain:
            return "Coleção não carregada."
        try:
            return self.chain.invoke(question)
        except Exception as e:
            return f"Erro ao responder: {e}"
