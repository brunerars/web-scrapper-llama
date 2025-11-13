import streamlit as st
import os 
from service.scrapping import ScrappingService


def show():
    st.header("🔍Web Scrapping")
    scrapper = ScrappingService()

    with st.form("Scrapping_form"):
        url = st.text_input("URL do site:", placeholder="https://example.com")
        collection_name = st.text_input("Nome da coleção:", placeholder="minha_colecao")
        submit_button = st.form_submit_button("Iniciar Scraping")

        if submit_button and url and collection_name:
            with st.spinner("Extraindo o conteúdo..."):
                result = scrapper.scrape_website(url, collection_name)
                if result["success"]:
                    st.success(f"💎{result['files']} arquivos salvos!")
                else:
                    st.error(f"Erro durante o scraping: {result['error']}")

                    