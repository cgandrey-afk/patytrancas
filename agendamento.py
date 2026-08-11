import streamlit as st
from datetime import date

def render(salvar_agendamento_fn):
    """
    Renderiza a página de agendamento de horários com suporte responsivo a dispositivos móveis.
    """
    # CSS Customizado para o Formulário e Fundo Branco
    st.markdown("""
        <style>
        /* Container principal com fundo branco limpo */
        .agendamento-card {
            background-color: #ffffff !important;
            padding: 24px;
            border-radius: 18px;
            border: 1px solid #fce4ec;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.04);
            margin-bottom: 20px;
        }

        /* Força fundo branco dentro do st.form */
        div[data-testid="stForm"] {
            background-color: #ffffff !important;
            border: none !important;
            padding: 0 !important;
        }

        /* Ajustes de responsividade para telas pequenas (Celulares) */
        @media screen and (max-width: 768px) {
            .agendamento-card {
                padding: 14px !important;
            }

            /* Força as colunas do formulário a ficarem em pilha única bem alinhada */
            div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] {
                flex-direction: column !important;
                gap: 12px !important;
            }

            div[data-testid="stForm"] div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }

            /* Ajuste dos rótulos e campos de entrada */
            div[data-testid="stForm"] label {
                font-size: 0.85rem !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # Envolvemos o conteúdo no container com a classe CSS customizada
    with st.container():
        st.markdown('<div class="agendamento-card">', unsafe_allow_html=True)
        
        st.markdown('<h3 style="color: #e05297; margin-bottom: 5px; margin-top: 0;">🗓️ Agende seu Horário</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666; font-size: 0.9rem;">Preencha os dados abaixo para enviar sua solicitação de agendamento.</p>', unsafe_allow_html=True)
        st.divider()

        with st.form("form_agendamento_cliente", border=False):
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

            st.markdown("<br>", unsafe_allow_html=True)
            btn_enviar = st.form_submit_button("✨ Confirmar Solicitação de Agendamento", use_container_width=True)

            if btn_enviar:
                if not nome_cliente or not telefone_cliente:
                    st.error("Por favor, preencha o Nome e o WhatsApp para contato!")
                else:
                    salvar_agendamento_fn(nome_cliente, telefone_cliente, servico_escolhido, data_atendimento, horario_atendimento)
                    st.success(f"Obrigado, {nome_cliente}! Seu agendamento foi registrado com sucesso. Entraremos em contato via WhatsApp!")

        st.markdown('</div>', unsafe_allow_html=True)