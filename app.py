import streamlit as st
from config import aplicar_estilo
from views import cliente, ia_upload, admin

# Aplica configurações visuais
aplicar_estilo()

# Criando abas superiores (Muito melhor e mais intuitivo no celular!)
aba1, aba2, aba3 = st.tabs(["✨ Catálogo / Agendar", "📸 Trança com IA", "🔒 Área da Trancista"])

with aba1:
    cliente.render()

with aba2:
    ia_upload.render()

with aba3:
    admin.render()