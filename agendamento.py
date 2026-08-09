import streamlit as st
from datetime import date

def render(salvar_agendamento_fn):
    """
    Renderiza a página de agendamento de horários.
    """
    with st.container(border=True):
        st.markdown('<h3 style="color: #e05297; margin-bottom: 5px;">🗓️ Agende seu Horário</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666; font-size: 0.9rem;">Preencha os dados abaixo para enviar sua solicitação de agendamento.</p>', unsafe_allow_html=True)
        st.divider()

        with st.form("form_agendamento_cliente"):
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                nome_cliente = st.text_input("Seu Nome Completo:")
                servico_escolhido = st.selectbox("Escolha o Estilo de Trança:", [
                    "Tranças Box Braids",
                    "Nagô Desenhada / Lateral",
                    "Goddess Braids / Bohemian",
                    "Gypsy Braids",
                    "Fulani Braids",
                    "Entrelace / Crochet Braids",
                    "Outro / Atendimento Personalizado"
                ])
                
            with col_f2:
                telefone_cliente = st.text_input("Seu WhatsApp / Telefone:", placeholder="(19) 99999-9999")
                
                c_d, c_h = st.columns(2)
                with c_d:
                    data_atendimento = st.date_input("Data do Atendimento:", min_value=date.today())
                with c_h:
                    horario_atendimento = st.selectbox("Horário:", ["08:00", "09:00", "10:30", "13:00", "14:30", "16:00"])

            btn_enviar = st.form_submit_button("✨ Confirmar Solicitação de Agendamento")

            if btn_enviar:
                if not nome_cliente or not telefone_cliente:
                    st.error("Por favor, preencha o Nome e o WhatsApp para contato!")
                else:
                    salvar_agendamento_fn(nome_cliente, telefone_cliente, servico_escolhido, data_atendimento, horario_atendimento)
                    st.success(f"Obrigado, {nome_cliente}! Seu agendamento foi registrado com sucesso. Entraremos em contato via WhatsApp!")