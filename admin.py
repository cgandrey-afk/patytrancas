import streamlit as st
import pandas as pd
from datetime import datetime

def render(db, carregar_agendamentos_fn, atualizar_status_fn, deletar_agendamento_fn):
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
                
                st.markdown('<div class="botoes-acao">', unsafe_allow_html=True)
                btn_entrar = st.form_submit_button("Entrar no Painel", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
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
                    
                    st.markdown('<div class="botoes-acao">', unsafe_allow_html=True)
                    btn_salvar_tranca = st.form_submit_button("Salvar Trança", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    if btn_salvar_tranca:
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
                st.write("### 📅 Gestão de Horários e Agenda")
                
                sub_tab1, sub_tab2, sub_tab3 = st.tabs([
                    "🔓 Abrir Agenda", 
                    "⚙️ Gerenciar Agenda", 
                    "➕ Agendar Cliente"
                ])

                # --- SUB-ABA 1: ABRIR AGENDA ---
                with sub_tab1:
                    st.write("#### 🔓 Abrir Horários para uma Data")
                    st.caption("Cadastre os horários livres em que você atenderá neste dia.")
                    
                    with st.form("form_abrir_agenda"):
                        data_abrir = st.date_input("Data do Expediente:", key="data_abrir_agenda")
                        horarios_texto = st.text_input(
                            "Horários disponíveis (separados por vírgula):", 
                            value="08:00, 09:30, 11:00, 13:30, 15:00, 16:30",
                            placeholder="ex: 08:00, 10:00, 14:00"
                        )
                        
                        st.markdown('<div class="botoes-acao">', unsafe_allow_html=True)
                        btn_salvar_agenda = st.form_submit_button("💾 Salvar Horários na Agenda", use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        if btn_salvar_agenda:
                            lista_h = [h.strip() for h in horarios_texto.split(",") if h.strip()]
                            if lista_h:
                                db.collection("agenda").document(str(data_abrir)).set({
                                    "data": str(data_abrir),
                                    "horarios_disponiveis": lista_h,
                                    "atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M")
                                })
                                st.success(f"Agenda para {data_abrir.strftime('%d/%m/%Y')} aberta com sucesso com {len(lista_h)} horários!")
                            else:
                                st.error("Insira pelo menos um horário válido.")

                # --- SUB-ABA 2: GERENCIAR AGENDA ---
                with sub_tab2:
                    st.write("#### ⚙️ Dias com Agenda Aberta")
                    st.caption("Consulte os horários configurados no banco e remova/bloqueie datas se necessário.")
                    
                    try:
                        docs_agenda = db.collection("agenda").stream()
                        lista_agenda = [doc.to_dict() for doc in docs_agenda]
                        
                        if lista_agenda:
                            for item in lista_agenda:
                                data_str = item.get("data", "")
                                horarios_arr = item.get("horarios_disponiveis", [])
                                horarios_str = ", ".join(horarios_arr) if horarios_arr else "Nenhum horário livre"
                                
                                with st.expander(f"📅 Data: {data_str} ({len(horarios_arr)} horários)"):
                                    st.write(f"**Horários cadastrados:** `{horarios_str}`")
                                    if st.button(f"🗑️ Excluir Agenda de {data_str}", key=f"del_agenda_{data_str}"):
                                        db.collection("agenda").document(data_str).delete()
                                        st.warning(f"Agenda do dia {data_str} removida!")
                                        st.rerun()
                        else:
                            st.info("Nenhuma data foi configurada na agenda ainda.")
                    except Exception as e:
                        st.error(f"Erro ao carregar dados da agenda: {e}")

                # --- SUB-ABA 3: AGENDAR CLIENTE MANUAL ---
                with sub_tab3:
                    st.write("#### ➕ Inserir Agendamento Manual (WhatsApp/Presencial)")
                    st.caption("Use esta opção quando a cliente fechar o agendamento diretamente com você.")
                    
                    with st.form("form_agendar_manual_admin"):
                        c_m1, c_m2 = st.columns(2)
                        with c_m1:
                            nome_manual = st.text_input("Nome da Cliente:")
                            tel_manual = st.text_input("Telefone / WhatsApp:", placeholder="(19) 99999-9999")
                            servico_manual = st.text_input("Serviço / Estilo de Trança:", placeholder="ex: Box Braids")
                        
                        with c_m2:
                            data_manual = st.date_input("Data do Atendimento:", key="data_manual_admin")
                            horario_manual = st.text_input("Horário Combinado:", placeholder="ex: 09:00")
                            status_manual = st.selectbox("Status Inicial:", ["Confirmado", "Pendente"])

                        st.markdown('<div class="botoes-acao">', unsafe_allow_html=True)
                        btn_salvar_manual = st.form_submit_button("📌 Confirmar Agendamento Manual", use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        if btn_salvar_manual:
                            if nome_manual and tel_manual:
                                db.collection("agendamentos").add({
                                    "cliente_nome": nome_manual,
                                    "cliente_telefone": tel_manual,
                                    "servico": servico_manual or "Não especificado",
                                    "data_agendamento": str(data_manual),
                                    "horario": horario_manual or "A combinar",
                                    "status": status_manual,
                                    "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M")
                                })
                                st.success(f"Agendamento de {nome_manual} cadastrado com sucesso!")
                                st.rerun()
                            else:
                                st.error("Preencha ao menos o Nome e o WhatsApp da cliente.")