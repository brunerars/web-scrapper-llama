# 🚀 Chat Avançado - Documentação Técnica

## 📋 Visão Geral

O **Chat Avançado** é uma versão otimizada do sistema RAG, especialmente projetada para desenvolvedores que trabalham com documentação técnica. Esta versão inclui melhorias significativas em memória, contexto e qualidade de respostas.

---

## ✨ Novas Features

### 🧠 1. Memória Conversacional
- **O que é**: O assistente agora lembra do contexto da conversa
- **Benefício**: Perguntas de follow-up funcionam naturalmente
- **Exemplo**:
  ```
  Você: "Como autenticar na API?"
  Bot: [explica autenticação]

  Você: "E se eu quiser usar OAuth?"  ← Entende que "isso" = autenticação
  Bot: [explica OAuth no contexto da pergunta anterior]
  ```

### 📚 2. Citações com Fontes
- **O que é**: Cada resposta mostra de quais arquivos a informação foi extraída
- **Benefício**: Rastreabilidade e verificação fácil
- **Exemplo de saída**:
  ```
  📚 Fontes consultadas:
  - page_1.md
  - page_3.md
  ```

### 💻 3. Code-Aware Chunking
- **O que é**: Algoritmo inteligente que preserva blocos de código inteiros
- **Benefício**: Exemplos de código não são cortados no meio
- **Detalhes técnicos**:
  - Chunk size: 1200 caracteres (vs 1000 antes)
  - Overlap: 300 caracteres (vs 200)
  - Separadores customizados para markdown e código

### 🎯 4. Prompt Especializado
- **O que é**: Prompt otimizado para documentação técnica
- **Características**:
  - ✅ Precisão técnica como prioridade
  - ✅ Sempre inclui exemplos de código quando relevante
  - ✅ Usa formatação markdown apropriada
  - ✅ Syntax highlighting automático
  - ✅ Contexto conversacional integrado

### ⚡ 5. Streaming de Respostas
- **O que é**: Respostas aparecem em tempo real, palavra por palavra
- **Benefício**: UX mais fluida, parece mais natural
- **Implementação**: `ask_question_stream()` com yield

### 🔍 6. Retrieval Avançado (MMR)
- **O que é**: Maximum Marginal Relevance - algoritmo que balanceia relevância e diversidade
- **Benefícios**:
  - Recupera documentos relevantes MAS diversos
  - Evita recuperar 7 chunks do mesmo documento
  - Melhor cobertura da documentação
- **Configuração**:
  - k=7 documentos recuperados (vs 3 antes)
  - fetch_k=20 (busca 20, filtra para os 7 melhores)
  - lambda_mult=0.7 (70% relevância, 30% diversidade)

### 🎛️ 7. Controles de Gerenciamento
- **Limpar Memória**: Remove histórico conversacional mantendo a coleção
- **Nova Conversa**: Limpa mensagens e memória completamente
- **Resumo de Histórico**: Visualize últimas interações

---

## 🏗️ Arquitetura

### Estrutura de Arquivos
```
service/
├── rag.py              # Versão original (simples)
└── advanced_rag.py     # Nova versão avançada ⭐

presentation/
├── chat.py             # Interface simples
└── advanced_chat.py    # Interface avançada ⭐
```

### Fluxo de Dados

```
Usuário digita pergunta
       ↓
advanced_chat.py recebe input
       ↓
advanced_rag.py processa:
  1. Recupera memória conversacional
  2. Busca documentos relevantes (MMR, k=7)
  3. Formata documentos com fontes
  4. Injeta no prompt especializado
  5. Envia para LLM (Groq)
  6. Stream da resposta
       ↓
Interface mostra resposta em tempo real
       ↓
Salva interação na memória
```

---

## 🔧 Componentes Técnicos

### AdvancedRAGService

**Principais Métodos:**

```python
# Carregar coleção de documentos
load_collection(collection_name: str) -> bool

# Fazer pergunta (modo síncrono)
ask_question(question: str) -> str

# Fazer pergunta com streaming
ask_question_stream(question: str) -> Iterator[str]

# Buscar documentos relevantes
get_relevant_docs(question: str, k: int = 5) -> List[Dict]

# Limpar memória
clear_memory() -> None

# Ver resumo da memória
get_memory_summary() -> str
```

### Configurações Importantes

**Embeddings:**
- Modelo: `all-MiniLM-L6-v2`
- Normalização: Ativada
- Device: CPU

**LLM:**
- Provider: Groq
- Modelo: `llama-3.1-8b-instant`
- Temperature: 0.1 (baixa para precisão)
- Streaming: Ativado

**Memória:**
- Tipo: `ConversationBufferMemory`
- Limite: 2000 tokens
- Output Key: "answer"

**Text Splitter:**
- Chunk Size: 1200
- Overlap: 300
- Separadores: Customizados para código/markdown

**Retriever:**
- Tipo: MMR (Maximum Marginal Relevance)
- k: 7 documentos
- fetch_k: 20 candidatos
- lambda_mult: 0.7

---

## 📊 Comparação: Simples vs Avançado

| Feature | Chat Simples | Chat Avançado |
|---------|--------------|---------------|
| Memória Conversacional | ❌ Não | ✅ Sim (2000 tokens) |
| Citações de Fontes | ❌ Não | ✅ Sim |
| Documentos Recuperados | 3 | 7 (com MMR) |
| Streaming | ❌ Não | ✅ Sim |
| Prompt | Básico | Especializado p/ docs técnicas |
| Chunking | Padrão (1000/200) | Code-aware (1200/300) |
| Diversidade de Docs | Simples similarity | MMR balanceado |
| Controles | Só limpar chat | Limpar memória + chat |
| Histórico Visível | ❌ Não | ✅ Sim |

---

## 🎮 Como Usar

### Modo Básico

1. **Selecione uma coleção** na barra lateral
2. Escolha **"💬 Chat Avançado"** no modo
3. Aguarde carregar a documentação
4. Digite sua pergunta e pressione Enter
5. Veja a resposta aparecer em tempo real

### Perguntas de Follow-up

```
Pergunta 1: "Como instalar a biblioteca?"
Resposta: [instruções de instalação]

Pergunta 2: "E quais são os requisitos?"  ← Contexto mantido!
Resposta: [requisitos, sabendo que é sobre a biblioteca anterior]

Pergunta 3: "Me dê um exemplo básico"  ← Ainda no contexto!
Resposta: [exemplo de uso da biblioteca]
```

### Gerenciamento de Memória

**Quando limpar a memória:**
- ✅ Ao mudar de tópico completamente
- ✅ Se as respostas ficarem confusas (muito contexto)
- ✅ Ao começar uma nova sessão de trabalho

**Quando limpar a conversa:**
- ✅ Para começar do zero
- ✅ Ao trocar de coleção
- ✅ Para remover mensagens antigas da tela

---

## 💡 Exemplos de Perguntas Ideais

### ✅ Boas Perguntas

```
"Como autenticar usando JWT nesta API?"
"Qual a diferença entre os métodos sync e async?"
"Me mostre um exemplo de uso do hook useEffect"
"Quais parâmetros a função createUser aceita?"
"Como fazer upload de arquivos?"
"Existe rate limiting na API?"
```

### 🎯 Perguntas que Aproveitam a Memória

```
Pergunta 1: "Como criar um usuário?"
Pergunta 2: "E como deletar?"  ← Entende que é sobre usuários
Pergunta 3: "Posso fazer isso em batch?"  ← Contexto mantido
Pergunta 4: "Quais são as limitações?"  ← Ainda no contexto
```

### 📝 Perguntas Comparativas

```
"Qual a diferença entre REST e GraphQL nesta lib?"
"Quando usar fetch vs axios aqui?"
"Comparar autenticação por token vs session"
```

---

## 🔍 Troubleshooting

### Respostas Fora de Contexto

**Problema**: O assistente está respondendo com base em conversas antigas
**Solução**: Clique em "🧹 Limpar Memória" na sidebar

### Respostas Muito Genéricas

**Problema**: Respostas não específicas da sua documentação
**Solução**:
- Verifique se a coleção está carregada corretamente
- Tente perguntas mais específicas
- Mencione termos-chave da sua documentação

### Streaming Travou

**Problema**: Resposta parou no meio
**Solução**:
- Aguarde alguns segundos (pode ser latência)
- Clique em "🗑️ Nova Conversa" e tente novamente
- Verifique sua conexão de internet

### Fontes Não Aparecem

**Problema**: Resposta sem citações
**Solução**: Isso é normal quando a resposta vem da memória ou quando não há match nos documentos. Tente reformular a pergunta.

---

## ⚙️ Configurações Avançadas

### Ajustar Temperatura do LLM

Edite `service/advanced_rag.py:17`:
```python
temperature=0.1  # Mais baixo = mais determinístico (0-1)
```

### Alterar Número de Documentos

Edite `service/advanced_rag.py:126-131`:
```python
search_kwargs={
    "k": 7,        # Número de documentos finais
    "fetch_k": 20, # Candidatos iniciais
}
```

### Modificar Limite de Memória

Edite `service/advanced_rag.py:75`:
```python
max_token_limit=2000  # Tokens de histórico mantidos
```

### Customizar Prompt

Edite o prompt em `service/advanced_rag.py:147-173`

---

## 📈 Próximas Melhorias (Roadmap)

### Curto Prazo
- [ ] Export de conversas para Markdown
- [ ] Pesquisa semântica visual (mostrar docs antes de perguntar)
- [ ] Feedback de relevância (👍👎)
- [ ] Histórico persistente (salvar conversas)

### Médio Prazo
- [ ] Multi-query retrieval (gerar variações da pergunta)
- [ ] Re-ranking com cross-encoder
- [ ] Sugestões de perguntas relacionadas
- [ ] Citações com trechos exatos destacados

### Longo Prazo
- [ ] RAG Fusion (combinar múltiplas estratégias)
- [ ] HyDE (Hypothetical Document Embeddings)
- [ ] Agente autônomo com ferramentas
- [ ] Integração com web search para docs externas
- [ ] Summarização de conversas longas

---

## 🤝 Contribuindo

Ideias de melhorias? Abra uma issue ou PR!

**Áreas de interesse:**
- Melhorias de performance
- Novos algoritmos de retrieval
- Integrações com outras ferramentas
- UI/UX enhancements

---

## 📚 Referências

- [LangChain Documentation](https://python.langchain.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Groq API](https://groq.com/)
- [Streamlit](https://streamlit.io/)
- [Maximum Marginal Relevance](https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf)

---

**Desenvolvido com ❤️ para desenvolvedores por desenvolvedores**
