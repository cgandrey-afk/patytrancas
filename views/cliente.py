import streamlit as st
from firebase_config import buscar_trancas, buscar_horarios_livres, salvar_agendamento
from utils import formatar_tempo

def render():
    st.title("✨ Agende seu Horário")
    st.subheader("Escolha o estilo desejado:")

    trancas = buscar_trancas()
    
    # Exibição do catálogo de tranças
    for tranca in trancas:
        with st.container():
            st.image(tranca["imagem"], use_container_width=True)
            st.markdown(f"### {tranca['nome']}")
            st.write(f"⏱️ **Tempo estimado:** {formatar_tempo(tranca['tempo_min'])}")
            st.write(f"💰 **Valor médio:** {tranca['preco']}")
            
            if st.button(f"Agendar {tranca['nome']}", key=f"btn_{tranca['id']}"):
                st.session_state['tranca_selecionada'] = tranca
                st.rerun()
            st.divider()

    # Formulário de confirmação de agendamento
    if 'tranca_selecionada' in st.session_state:
        st.markdown("---")
        st.subheader("🗓️ Finalizar Agendamento")
        tranca = st.session_state['tranca_selecionada']
        st.info(f"Selecionado: **{tranca['nome']}** ({formatar_tempo(tranca['tempo_min'])})")
        
        data = st.date_input("Escolha a data")
        horario = st.selectbox("Escolha o horário", buscar_horarios_livres())
        nome = st.text_input("Seu Nome")
        whatsapp = st.text_input("Seu WhatsApp")
        
        if st.button("Confirmar Agendamento"):
            if nome and whatsapp:
                salvar_agendamento({"tranca": tranca['nome'], "data": str(data), "horario": horario, "nome": nome, "whatsapp": whatsapp})
                st.success("Agendamento realizado com sucesso! Entraremos em contato para confirmar.")
                del st.session_state['tranca_selecionada']
            else:
                st.warning("Por favor, preencha todos os campos.")