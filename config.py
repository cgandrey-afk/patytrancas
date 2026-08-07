import streamlit as st

def aplicar_estilo():
    st.set_page_config(
        page_title="Agendamento de Tranças",
        page_icon="✂️",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # CSS para otimizar visualização em telas móveis
    st.markdown("""
        <style>
        /* Oculta menus padrão do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Ajusta margens superiores para mobile */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        /* Botões em largura total para facilitar o toque */
        .stButton > button {
            width: 100%;
            border-radius: 12px;
            height: 3em;
            font-weight: bold;
            background-color: #E91E63;
            color: white;
            border: none;
        }
        
        /* Cards estilizados para as tranças */
        .tranca-card {
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            border: 1px solid #e0e0e0;
        }
        </style>
    """, unsafe_allow_html=True)