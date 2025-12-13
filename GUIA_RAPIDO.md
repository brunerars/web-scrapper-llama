# 🚀 Guia Rápido - Chat Avançado

## ⚡ Como Testar as Novas Features

### 1️⃣ Iniciar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá em: `http://localhost:8501`

---

### 2️⃣ Escolher o Modo Avançado

Na **barra lateral**, você verá 3 modos:

- **💬 Chat Avançado** ← Escolha este! (Nova versão)
- Chat Simples (Versão original)
- 🔍 Scrapping (Para criar novas coleções)

---

### 3️⃣ Selecionar uma Coleção

Clique no botão **"Usar"** ao lado da coleção que deseja consultar.

Exemplo: Se você tem a coleção "Agno", clique em "Usar" ao lado dela.

---

### 4️⃣ Testar as Novas Features

#### 🧠 Testar Memória Conversacional

```
Pergunta 1: "O que é esta documentação?"
Pergunta 2: "Me dê mais detalhes sobre isso"  ← Vai lembrar do contexto!
Pergunta 3: "E como eu uso?"  ← Continua lembrando!
```

#### 📚 Ver Citações com Fontes

Após qualquer resposta, role até o final e você verá:

```
📚 Fontes consultadas:
- page_1.md
- page_3.md
```

Isso mostra de quais arquivos a informação veio!

#### ⚡ Ver Streaming em Ação

As respostas aparecem **palavra por palavra em tempo real**, não tudo de uma vez.

#### 💻 Testar Code-Aware

Pergunte algo sobre código, exemplo:

```
"Me mostre um exemplo de código de autenticação"
"Como implementar esta função?"
```

O código virá formatado com syntax highlighting!

---

### 5️⃣ Usar os Controles

Na **barra lateral**, você encontra:

#### 🧹 Limpar Memória
- Clique quando quiser começar um novo assunto
- Mantém a coleção carregada
- Remove histórico de conversas anteriores

#### 🗑️ Nova Conversa
- Limpa tudo (mensagens + memória)
- Use para começar completamente do zero

#### 📝 Histórico da Conversa
- Clique para expandir
- Veja um resumo das últimas interações

---

## 💡 Exemplos de Perguntas para Testar

### Para Documentação Técnica

```
"Como instalar?"
"Quais são os requisitos?"
"Me dê um exemplo de uso"
"Qual a diferença entre X e Y?"
"Como fazer autenticação?"
```

### Perguntas Sequenciais (Testa Memória)

```
1. "O que é esta ferramenta?"
2. "Como eu instalo isso?"  ← Sabe que "isso" = a ferramenta
3. "Quais são as dependências?"  ← Contexto mantido
4. "Me dê um exemplo básico"  ← Ainda no contexto!
```

### Perguntas Técnicas

```
"Explique a arquitetura do sistema"
"Quais endpoints da API estão disponíveis?"
"Como fazer tratamento de erros?"
"Mostre exemplos de configuração"
```

---

## 🎯 Comparação Rápida

| O que testar | Como verificar |
|--------------|----------------|
| **Memória** | Faça perguntas de follow-up sem repetir contexto |
| **Citações** | Veja "📚 Fontes consultadas" no final da resposta |
| **Streaming** | Observe texto aparecendo palavra por palavra |
| **Código** | Peça exemplos e veja syntax highlighting |
| **Mais Contexto** | Respostas mais completas (7 docs vs 3) |
| **Controles** | Teste botões de limpar na sidebar |

---

## 🐛 Troubleshooting Rápido

### "Coleção não carregada"
**Solução**: Selecione uma coleção clicando em "Usar" na sidebar

### Respostas estranhas/fora de contexto
**Solução**: Clique em "🧹 Limpar Memória"

### Quer começar do zero
**Solução**: Clique em "🗑️ Nova Conversa"

### Resposta parou no meio
**Solução**: Aguarde alguns segundos ou recarregue a página

---

## 📊 Diferenças Visuais

### Chat Simples
```
[Pergunta do usuário]
[Resposta completa aparece de uma vez]
```

### Chat Avançado ⭐
```
[Pergunta do usuário]
[Resposta aparece palavra por palavra... ⚡]
[Com código formatado 💻]

📚 Fontes consultadas:
- page_1.md
- page_3.md
```

---

## 🎮 Fluxo de Uso Ideal

```
1. Abrir app → streamlit run app.py
2. Selecionar "💬 Chat Avançado"
3. Escolher coleção
4. Aguardar carregar documentação
5. Fazer primeira pergunta
6. Fazer perguntas de follow-up aproveitando a memória
7. Se mudar de assunto → "🧹 Limpar Memória"
8. Se quiser limpar tela → "🗑️ Nova Conversa"
```

---

## 🔥 Dica Pro

**Use perguntas progressivas para aproveitar a memória:**

```
❌ Ruim (repete contexto):
"Como instalar a biblioteca X?"
"Como configurar a biblioteca X após instalar?"
"Como usar a biblioteca X depois de configurar?"

✅ Bom (aproveita memória):
"Como instalar a biblioteca X?"
"E como configurar?"  ← Mais natural!
"Como eu uso ela agora?"  ← Melhor UX!
```

---

## 📈 Próximos Passos

Depois de testar, você pode:

1. **Criar suas próprias coleções** usando o modo "🔍 Scrapping"
2. **Ajustar configurações** em `service/advanced_rag.py` (temperatura, k docs, etc.)
3. **Customizar o prompt** para seu caso de uso específico
4. **Ver documentação completa** em `ADVANCED_FEATURES.md`

---

**Bom uso! 🚀**
