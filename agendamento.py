import streamlit as st
from datetime import date

def render(salvar_agendamento_fn):
    """
    Renderiza a página de agendamento usando componentes nativos leves e limpos.
    """
    st.markdown("""
        <style>
        /* Container Principal */
        .agendamento-card {
            background-color: #ffffff !important;
            padding: 24px;
            border-radius: 20px;
            border: 1px solid #f2c4ce;
            box-shadow: 0px 6px 20px rgba(224, 82, 151, 0.08);
            margin: 0 auto 20px auto;
            max-width: 850px;
            width: 100%;
        }

        /* Estilo dos Labels */
        .agendamento-card label, 
        div[data-testid="stForm"] label,
        div[data-testid="stForm"] label p {
            color: #262730 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }

        /* Inputs de Texto e Data com fundo claro e borda rosa */
        div[data-testid="stForm"] input {
            background-color: #ffffff !important;
            color: #262730 !important;
            border: 1.5px solid #f2c4ce !important;
            border-radius: 10px !important;
            min-height: 45px !important;
        }

        /* Radio Buttons estilo Chips/Pills (Opções de Trança e Horário) */
        div[data-testid="stForm"] div[role="radiogroup"] {
            gap: 8px !important;
        }
        
        div[data-testid="stForm"] div[role="radiogroup"] label {
            background-color: #fdf8fa !important;
            border: 1px solid #f2c4ce !important;
            padding: 8px 14px !important;
            border-radius: 20px !important;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        div[data-testid="stForm"] div[role="radiogroup"] label:hover {
            border-color: #e05297 !important;
            background-color: #fce8f0 !important;
        }

        /* Botão do formulário */
        div[data-testid="stForm"] button[kind="primaryFormSubmit"],
        div[data-testid="stForm"] button {
            background-color: #e05297 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 20px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            box-shadow: 0px 4px 12px rgba(224, 82, 151, 0.25) !important;
            width: 100% !important;
            min-height: 48px !important;
            margin-top: 15px !important;
            cursor: pointer;
        }

        div[data-testid="stForm"] button:hover {
            background-color: #c93b7f !important;
        }

        /* --- RESPONSIVIDADE CELULAR --- */
        @media screen and (max-width: 768px) {
            .agendamento-card {
                padding: 16px 12px !important;
            }

            div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] {
                display: flex !important;
                flex-direction: column !important;
                gap: 12px !important;
                width: 100% !important;
            }

            div[data-testid="stForm"] div[data-testid="column"],
            div[data-testid="stForm"] div[data-testid="stColumn"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
                padding: 0 !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="agendamento-card">', unsafe_allow_html=True)
    
    st.markdown('<h3 style="color: #e05297; margin-bottom: 5px; margin-top: 0; text-align: center;">🗓️ Agende seu Horário</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #555555; font-size: 0.88rem; text-align: center; margin-bottom: 20px;">Preencha os dados abaixo para enviar sua solicitação de agendamento.</p>', unsafe_allow_html=True)

    with st.form("form_agendamento_cliente", border=False):
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            nome_cliente = st.text_input("Seu Nome Completo:", placeholder="Digite seu nome completo")
            telefone_cliente = st.text_input("Seu WhatsApp / Telefone:", placeholder="(19) 99999-9999")
            
        with col_f2:
            data_atendimento = st.date_input("Data do Atendimento:", min_value=date.today())
            horario_atendimento = st.select_slider(
                "Horário de Atendimento:",
                options=["08:00", "09:00", "10:30", "13:00", "14:30", "16:00"]
            )

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Substituído por st.radio para não ter o bug de dropdown do Streamlit
        servico_escolhido = st.radio(
            "Escolha o Estilo de Trança:",
            options=[
                "Box Braids",
                "Nagô Desenhada / Lateral",
                "Goddess Braids / Bohemian",
                "Gypsy Braids",
                "Fulani Braids",
                "Entrelace / Crochet Braids",
                "Outro / Personalizado"
            ],
            horizontal=True
        )

        btn_enviar = st.form_submit_button("✨ Confirmar Solicitação de Agendamento")

        if btn_enviar:
            if not nome_cliente or not telefone_cliente:
                st.error("Por favor, preencha o Nome e o WhatsApp para contato!")
            else:
                salvar_agendamento_fn(nome_cliente, telefone_cliente, servico_escolhido, data_atendimento, horario_atendimento)
                st.success(f"Obrigado, {nome_cliente}! Seu agendamento foi registrado com sucesso. Entraremos em contato via WhatsApp!")

    st.markdown('</div>', unsafe_allow_html=True)