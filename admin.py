import streamlit as st
import pandas as pd
from datetime import datetime

def render(db, carregar_agendamentos_fn, atualizar_status_fn, deletar_agendamento_fn):
    # -------------------------------------------------------------
    # CSS DEDICADO: RESPONSIVIDADE E ESTILIZAÇÃO DO ADMIN
    # -------------------------------------------------------------
    st.markdown("""
        <style>
        /* Força fundo branco em formulários, caixas, abas e inputs */
        [data-testid="stForm"], 
        [data-testid="stVerticalBlockBorderWrapper"],
        div[data-baseweb="tab-list"],
        div[data-baseweb="tab-panel"] {
            background-color: #ffffff !important;
            border-radius: 12px !important;
        }
        
        /* Ajusta o contraste dos rótulos e textos */
        .stMarkdown, label, p, h1, h2, h3, h4 {
            color: #262626 !important;
        }
        
        /* Destaque rosa nos títulos de seção */
        .admin-title {
            color: #e05297 !important;
            font-weight: 700;
            margin-bottom: 4px;
        }

        /* Estilização dos botões para preenchimento total e alinhamento */
        div.stButton > button {
            width: 100% !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }

        /* AJUSTE RESPONSIVO PARA SMARTPHONES (TELAS < 768px) */
        @media screen and (max-width: 768px) {
            /* Faz com que colunas de ações fiquem em bloco ou empilhadas de forma limpa */
            .admin-actions-container {
                display: flex !important;
                flex-direction: column !important;
                gap: 10px !important;
            }
            
            /* Ajuste de margem dos botões em telas pequenas */
            div[data-testid="stColumn"] {
                width: 100% !important;
                margin-bottom: 5px !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # CONTAINER PRINCIPAL NATIVO (CAIXA BRANCA COM BORDA)
    # -------------------------------------------------------------
    with st.container(border=True):
        st.markdown('<h2 class="admin-title">🔒 Área Administrativa</h2>', unsafe_allow_html=True)
        st.write("Gerencie os modelos do catálogo, horários de atendimento e solicitações de clientes.")
        st.divider()

        # Controle de Autenticação na Sessão
        if 'autenticado' not in st.session_state:
            st.session_state['autenticado'] = False

        if not st.session_state['autenticado']:
            st.subheader("🔑 Login de Acesso")
            
            with st.form("form_login_admin"):
                senha = st.text_input("Senha de acesso:", type="password")
                btn_entrar = st.form_submit_button("Entrar no Painel", use_container_width=True)
                
                if btn_entrar:
                    if senha == "12345":
                        st.session_state['autenticado'] = True
                        st.success("Acesso liberado!")
                        st.rerun()
                    else:
                        st.error("Senha incorreta!")
        else:
            # Cabeçalho do usuário logado
            col_header1, col_header2 = st.columns([3, 1])
            with col_header1:
                st.success("Bem-vinda de volta, Paty!")
            with col_header2:
                if st.button("🚪 Sair", use_container_width=True):
                    st.session_state['autenticado'] = False
                    st.rerun()

            st.write("")

            # NAVEGAÇÃO POR ABAS
            tab1, tab2, tab3 = st.tabs([
                "📋 Agenda & Solicitações", 
                "➕ Cadastrar Trança", 
                "📅 Gerenciar Horários"
            ])

            # -----------------------------------------------------------
            # ABA 1: Agendamentos Recebidos
            # -----------------------------------------------------------
            with tab1:
                st.write("### 📋 Solicitações no Banco de Dados")
                
                df_agendamentos = carregar_agendamentos_fn()

                if not df_agendamentos.empty:
                    total = len(df_agendamentos)
                    pendentes = len(df_agendamentos[df_agendamentos['status'] == 'Pendente']) if 'status' in df_agendamentos.columns else 0
                    confirmados = len(df_agendamentos[df_agendamentos['status'] == 'Confirmado']) if 'status' in df_agendamentos.columns else 0

                    m1, m2, m3 = st.columns(3)
                    m1.metric("Total", total)
                    m2.metric("Pendentes ⏳", pendentes)
                    m3.metric("Confirmados ✅", confirmados)

                    st.divider()
                    
                    st.dataframe(
                        df_agendamentos.rename(columns={
                            "id": "ID Documento",
                            "cliente_nome": "Cliente",
                            "cliente_telefone": "Telefone",
                            "servico": "Serviço",
                            "data_agendamento": "Data",
                            "horario": "Horário",
                            "status": "Status",
                            "criado_em": "Criado em"
                        }),
                        use_container_width=True,
                        hide_index=True
                    )

                    st.divider()
                    st.write("#### ⚙️ Alterar Status ou Deletar Registros")
                    
                    # Organização em 2 blocos para melhor fluxo visual
                    col_inputs, col_botoes = st.columns([2, 1])
                    
                    with col_inputs:
                        c_id, c_status = st.columns(2)
                        with c_id:
                            id_selecionado = st.selectbox("ID do Agendamento:", df_agendamentos['id'].tolist())
                        with c_status:
                            novo_status = st.selectbox("Novo Status:", ["Pendente", "Confirmado", "Concluído", "Cancelado"])
                    
                    with col_botoes:
                        st.write("<span style='font-size:0.8rem; opacity:0;'>Ações</span>", unsafe_allow_html=True)
                        btn_c1, btn_c2 = st.columns(2)
                        with btn_c1:
                            if st.button("Atualizar", use_container_width=True):
                                atualizar_status_fn(id_selecionado, novo_status)
                                st.success("Atualizado!")
                                st.rerun()
                        with btn_c2:
                            if st.button("🗑️ Excluir", use_container_width=True):
                                deletar_agendamento_fn(id_selecionado)
                                st.warning("Removido!")
                                st.rerun()
                else:
                    st.info("Nenhum agendamento registrado até o momento.")

            # -----------------------------------------------------------
            # ABA 2: Cadastrar Modelo de Trança
            # -----------------------------------------------------------
            with tab2:
                st.write("### ➕ Novo Modelo de Trança")
                with st.form("form_novo_modelo"):
                    nome = st.text_input("Nome do Modelo")
                    tempo = st.number_input("Tempo Padrão (em minutos)", step=30, value=180)
                    preco = st.text_input("Preço Estimado (ex: R$ 150,00)")
                    imagem = st.file_uploader("Foto da Trança", type=["jpg", "jpeg", "png"])
                    
                    if st.form_submit_button("Salvar Trança", use_container_width=True):
                        if nome and preco:
                            db.collection("catalogo").add({
                                "nome": nome,
                                "tempo_minutos": tempo,
                                "preco": preco,
                                "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M")
                            })
                            st.success(f"Modelo '{nome}' cadastrado com sucesso!")
                        else:
                            st.error("Preencha o nome e o preço antes de salvar.")

            # -----------------------------------------------------------
            # ABA 3: Gerenciar Horários
            # -----------------------------------------------------------
            with tab3:
                st.write("### 📅 Gerenciar Horários Livres")
                with st.form("form_horarios_livres"):
                    data_trabalho = st.date_input("Data do Expediente")
                    horarios = st.text_input("Horários disponíveis (separados por vírgula)", value="08:00, 13:00, 17:00")
                    
                    if st.form_submit_button("Atualizar Agenda", use_container_width=True):
                        lista_horarios = [h.strip() for h in horarios.split(",") if h.strip()]
                        db.collection("agenda").document(str(data_trabalho)).set({
                            "data": str(data_trabalho),
                            "horarios_disponiveis": lista_horarios
                        })
                        st.success(f"Agenda para {data_trabalho} atualizada com sucesso!")