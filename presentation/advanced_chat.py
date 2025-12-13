import streamlit as st
from service.advanced_rag import AdvancedRAGService


def show():
    """Interface de chat avançada com memória e streaming."""

    st.header("💬 Chat Técnico com Documentação")

    # Verificar se há coleção selecionada
    if not st.session_state.collection:
        st.info("👈 **Selecione uma coleção na barra lateral** para começar.")
        st.markdown("""
        ### 🚀 Features do Chat Avançado:
        - 🧠 **Memória Conversacional** - Lembra do contexto da conversa
        - 📚 **Citações com Fontes** - Mostra de onde veio cada informação
        - 💻 **Code-Aware** - Entende e formata código corretamente
        - ⚡ **Respostas em Tempo Real** - Streaming para UX fluida
        - 🎯 **Otimizado para Devs** - Respostas técnicas e precisas
        """)
        return

    # Mostrar coleção selecionada
    st.success(f"📂 **Coleção**: `{st.session_state.collection}`")

    # Inicializar serviço RAG avançado
    if "advanced_rag_service" not in st.session_state:
        st.session_state.advanced_rag_service = AdvancedRAGService()

    # Carregar coleção se mudou
    if "current_collection" not in st.session_state or st.session_state.current_collection != st.session_state.collection:
        with st.spinner("🔄 Carregando documentação e criando índices..."):
            success = st.session_state.advanced_rag_service.load_collection(st.session_state.collection)

            if success:
                st.session_state.current_collection = st.session_state.collection
                st.success('✅ Documentação carregada com sucesso!')
            else:
                st.error('❌ Falha ao carregar documentação.')
                return

    # Sidebar com informações e controles
    with st.sidebar:
        st.divider()
        st.subheader("🎛️ Controles do Chat")

        # Botão para limpar memória
        if st.button("🧹 Limpar Memória", use_container_width=True):
            st.session_state.advanced_rag_service.clear_memory()
            st.success("Memória limpa!")

        # Botão para limpar conversa
        if st.button("🗑️ Nova Conversa", use_container_width=True):
            st.session_state.messages = []
            st.session_state.advanced_rag_service.clear_memory()
            st.rerun()

        # Mostrar resumo da memória
        with st.expander("📝 Histórico da Conversa"):
            summary = st.session_state.advanced_rag_service.get_memory_summary()
            st.markdown(summary)

        # Dicas de uso
        with st.expander("💡 Dicas de Uso"):
            st.markdown("""
            **Exemplos de perguntas:**
            - "Como faço para autenticar na API?"
            - "Qual a diferença entre X e Y?"
            - "Me dê um exemplo de uso do método Z"
            - "Como instalar essa biblioteca?"
            - "Quais são os parâmetros da função X?"

            **Features:**
            - Use perguntas de follow-up naturalmente
            - O assistente lembra do contexto
            - Peça exemplos de código
            - Solicite comparações entre conceitos
            """)

    # Container para mensagens
    st.divider()

    # Mostrar histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input de chat
    if prompt := st.chat_input("💬 Digite sua pergunta sobre a documentação..."):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Mostrar mensagem do usuário
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gerar resposta com streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Stream da resposta
            with st.spinner("🤔 Pensando..."):
                for chunk in st.session_state.advanced_rag_service.ask_question_stream(prompt):
                    full_response += chunk
                    # Atualizar placeholder com resposta parcial
                    message_placeholder.markdown(full_response + "▌")

            # Mostrar resposta final
            message_placeholder.markdown(full_response)

        # Salvar resposta no histórico
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Footer com estatísticas
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📨 Mensagens", len(st.session_state.messages))

    with col2:
        st.metric("💬 Interações", len(st.session_state.messages) // 2)

    with col3:
        st.metric("📚 Coleção", st.session_state.collection)
