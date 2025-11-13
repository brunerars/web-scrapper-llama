import os
import streamlit as st
from dotenv import load_dotenv
from presentation import scrapping
from presentation import chat

load_dotenv()
st.set_page_config(page_title="SCRAPPER DOCS", page_icon="🔥", layout="wide")
st.title("🔥SCRAPPER Documentation🔥")

with st.sidebar:
    st.header("Coleções")
    mode = st.radio("Modo:", ["Chat", "Scrapping"])
    st.divider()
    st.subheader("Coleções Disponíveis")
    collections_dir = "data/collections/"

    if os.path.exists(collections_dir):
        collections = [d for d in os.listdir(collections_dir) 
                        if os.path.isdir(os.path.join(collections_dir, d))]
        
        for collection in collections:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"- {collection}")
            with col2:
                if st.button("Usar", key=f"use_{collection}"):
                    st.session_state.collection = collection
                    st.rerun()


if "messages" not in st.session_state:
    st.session_state.messages = []
if "collection" not in st.session_state:
    st.session_state.collection = None


if mode == "Scrapping":
    scrapping.show()
else:
    chat.show()
                    