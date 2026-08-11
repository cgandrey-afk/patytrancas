import streamlit as st
from datetime import datetime, date

def render(db, salvar_agendamento_fn):
    """
    Renderiza a página de agendamento 100% dinâmica sincronizada com o banco de dados.
    """
    st.markdown('<div class="agendamento-card">', unsafe_allow_html=True)
    
    st.markdown('<h3 style="color: #e05297; margin-bottom: 5px; margin-top: 0; text-align: center;">🗓️ Agende seu Horário</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #555555; font-size: 0.88rem; text-align: center; margin-bottom: 20px;">Escolha uma das datas disponíveis abaixo destacadas em rosa.</p>', unsafe_allow_html=True)

    # 1. BUSCA DIAS DISPONÍVEIS NO FIREBASE
    agenda_disponivel = {}
    try:
        docs = db.collection("agenda").stream()
        for doc in docs:
            dados = doc.to_dict()
            data_str = dados.get("data")
            horarios = dados.get("horarios_disponiveis", [])
            if horarios: # Só exibe datas com pelo menos um horário livre
                agenda_disponivel[data_str] = horarios
    except Exception as e:
        st.error(f"Erro ao carregar datas disponíveis: {e}")

    # Inicializa estados no st.session_state
    if "data_selecionada" not in st.session_state:
        st.session_state["data_selecionada"] = None

    # 2. SELETOR VISUAL DE DATAS (CALENDÁRIO DINÂMICO)
    st.markdown("#### 1. Selecione um Dia Disponível:")
    
    if agenda_disponivel:
        datas_ordenadas = sorted(agenda_disponivel.keys())
        cols = st.columns(min(len(datas_ordenadas), 4)) # Até 4 colunas responsivas
        
        for idx, d_str in enumerate(datas_ordenadas):
            col = cols[idx % 4]
            # Formata data para exibição (ex: 15/08 - Sáb)
            data_obj = datetime.strptime(d_str, "%Y-%m-%d")
            data_formatada = data_obj.strftime("%d/%m")
            
            with col:
                btn_label = f"🌸 {data_formatada}"
                
                # Se for a data atualmente selecionada, dá destaque
                if st.session_state["data_selecionada"] == d_str:
                    btn_label = f"✅ {data_formatada}"

                if st.button(btn_label, key=f"btn_data_{d_str}", use_container_width=True):
                    st.session_state["data_selecionada"] = d_str
                    st.rerun()
    else:
        st.info("Nenhuma data aberta para agendamento no momento. Por favor, consulte novamente mais tarde!")

    st.divider()

    # 3. FORMULÁRIO DE AGENDAMENTO (SÓ APARECE APÓS A SELEÇÃO DO DIA)
    if st.session_state["data_selecionada"]:
        data_sel = st.session_state["data_selecionada"]
        horarios_livres = agenda_disponivel.get(data_sel, [])
        data_sel_pt = datetime.strptime(data_sel, "%Y-%m-%d").strftime("%d/%m/%Y")

        st.success(f"Data selecionada: **{data_sel_pt}**")

        st.markdown("#### 2. Complete com seus Dados e Escolha o Horário:")
        
        with st.form("form_agendamento_cliente", border=False):
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                nome_cliente = st.text_input("Seu Nome Completo:", placeholder="Digite seu nome completo")
                telefone_cliente = st.text_input("Seu WhatsApp / Telefone:", placeholder="(19) 99999-9999")
                
            with col_f2:
                horario_atendimento = st.selectbox(
                    "Horários Livres nesta Data:",
                    options=horarios_livres
                )

            st.markdown("<br>", unsafe_allow_html=True)
            
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

            # Isola o botão com a classe de ação definida no CSS
            st.markdown('<div class="botoes-acao">', unsafe_allow_html=True)
            btn_enviar = st.form_submit_button("✨ Confirmar Agendamento", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            if btn_enviar:
                if not nome_cliente or not telefone_cliente:
                    st.error("Por favor, preencha o Nome e o WhatsApp para contato!")
                else:
                    # Salva no Banco de Dados
                    salvar_agendamento_fn(
                        nome_cliente, 
                        telefone_cliente, 
                        servico_escolhido, 
                        data_sel, 
                        horario_atendimento
                    )
                    
                    # Remove o horário agendado da lista de horários disponíveis
                    horarios_restantes = [h for h in horarios_livres if h != horario_atendimento]
                    if horarios_restantes:
                        db.collection("agenda").document(data_sel).update({
                            "horarios_disponiveis": horarios_restantes
                        })
                    else:
                        db.collection("agenda").document(data_sel).delete()

                    st.success(f"Obrigado, {nome_cliente}! Agendamento confirmado para {data_sel_pt} às {horario_atendimento}.")
                    st.session_state["data_selecionada"] = None
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)