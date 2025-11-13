import streamlit as st
from service.rag import RAGService


def show():
    st.header("💬Chat com Documentos")
    if not st.session_state.collection:
        st.info("Por favor, selecione uma coleção na barra lateral para começar a usar o chat.")
        return
    st.success(f"📂 Coleção selecionada: **{st.session_state.collection}**")
    if "rag_service" not in st.session_state:
        st.session_state.rag_service = RAGService()

    if "current_collection" not in st.session_state or st.session_state.current_collection != st.session_state.collection:
        with st.spinner("Carregando documentos da coleção..."):
            success = st .session_state.rag_service.load_collection(st.session_state.collection)
            if success:
                st.session_state.current_collection = st.session_state.collection
                st.success('Documentos carregados com sucesso!')
                
            else:
                st.error('Falha ao carregar os documentos da coleção.')
                return
            

    for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
    if prompt := st.chat_input("Digite sua pergunta aqui..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = st.session_state.rag_service.ask_question(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)

    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()