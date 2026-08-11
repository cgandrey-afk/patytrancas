import streamlit as st
from datetime import date

def render(salvar_agendamento_fn):
    """
    Renderiza a página de agendamento de horários com cores fixas e layout responsivo.
    """
    st.markdown("""
        <style>
        /* Container principal com fundo branco e texto escuro */
        .agendamento-card {
            background-color: #ffffff !important;
            padding: 20px;
            border-radius: 18px;
            border: 1px solid #f2c4ce;
            box-shadow: 0px 4px 15px rgba(224, 82, 151, 0.08);
            margin-bottom: 20px;
        }

        /* Força todas as labels (textos acima dos inputs) a ficarem escuras e visíveis */
        .agendamento-card label, 
        div[data-testid="stForm"] label,
        div[data-testid="stForm"] label p {
            color: #262730 !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
        }

        /* Estilização dos Inputs (Caixas de texto, Selects, DatePicker) */
        div[data-testid="stForm"] input, 
        div[data-testid="stForm"] select,
        div[data-testid="stForm"] div[role="combobox"] {
            background-color: #fdf8fa !important;
            color: #262730 !important;
            border: 1px solid #f2c4ce !important;
            border-radius: 10px !important;
        }

        /* Texto dentro do input selecionado */
        div[data-testid="stForm"] input::placeholder {
            color: #888888 !important;
        }

        /* Botão do formulário */
        div[data-testid="stForm"] button[kind="primaryFormSubmit"],
        div[data-testid="stForm"] button {
            background-color: #e05297 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 10px 20px !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            box-shadow: 0px 4px 10px rgba(224, 82, 151, 0.2) !important;
            width: 100% !important;
        }

        div[data-testid="stForm"] button:hover {
            background-color: #c93b7f !important;
            color: #ffffff !important;
        }

        /* RESPONSIVIDADE PARA CELULAR (Telas pequenas) */
        @media screen and (max-width: 768px) {
            .agendamento-card {
                padding: 12px !important;
            }

            /* Desfaz a divisão de colunas e empilha tudo verticalmente */
            div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] {
                display: flex !important;
                flex-direction: column !important;
                gap: 10px !important;
                width: 100% !important;
            }

            div[data-testid="stForm"] div[data-testid="column"] {
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
    st.markdown('<p style="color: #555555; font-size: 0.88rem; text-align: center; margin-bottom: 15px;">Preencha os dados abaixo para enviar sua solicitação de agendamento.</p>', unsafe_allow_html=True)

    with st.form("form_agendamento_cliente", border=False):
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            nome_cliente = st.text_input("Seu Nome Completo:", placeholder="Digite seu nome")
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

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        btn_enviar = st.form_submit_button("✨ Confirmar Solicitação de Agendamento")

        if btn_enviar:
            if not nome_cliente or not telefone_cliente:
                st.error("Por favor, preencha o Nome e o WhatsApp para contato!")
            else:
                salvar_agendamento_fn(nome_cliente, telefone_cliente, servico_escolhido, data_atendimento, horario_atendimento)
                st.success(f"Obrigado, {nome_cliente}! Seu agendamento foi registrado com sucesso. Entraremos em contato via WhatsApp!")

    st.markdown('</div>', unsafe_allow_html=True)