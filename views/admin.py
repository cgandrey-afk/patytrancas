import streamlit as st
import pandas as pd
from datetime import datetime

def render(db, carregar_agendamentos_fn, atualizar_status_fn, deletar_agendamento_fn):
    # -------------------------------------------------------------
    # FORÇA O FUNDO BRANCO VIA CSS NA PÁGINA DO ADMIN
    # -------------------------------------------------------------
    st.markdown("""
        <style>
        /* Força a caixa do formulário e o container da página a ficarem com fundo branco */
        [data-testid="stForm"], 
        .stMarkdown, 
        div[data-testid="stVerticalBlock"] > div:has(div.admin-anchor) {
            background-color: #ffffff !important;
        }
        
        /* Cria um painel branco unificado para todo o conteúdo do Admin */
        .admin-box {
            background-color: #ffffff !important;
            padding: 24px !important;
            border-radius: 18px !important;
            box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.08) !important;
            border: 1px solid #f2c4ce !important;
            margin-bottom: 20px !important;
        }
        </style>
        <div class="admin-anchor"></div>
    """, unsafe_allow_html=True)

    # Início do bloco com fundo branco
    st.markdown('<div class="admin-box">', unsafe_allow_html=True)

    st.markdown("""
        <h2 style="color: #e05297; margin-bottom: 2px;">🔒 Área Administrativa</h2>
        <p style="color: #444; font-size: 0.9rem;">Gerencie os modelos do catálogo, horários de atendimento e solicitações de clientes.</p>
        <hr style="border: 0.5px solid #f2c4ce; margin: 12px 0 20px 0;">
    """, unsafe_allow_html=True)

    # Controle de Autenticação na Sessão
    if 'autenticado' not in st.session_state:
        st.session_state['autenticado'] = False

    if not st.session_state['autenticado']:
        st.subheader("🔑 Login de Acesso")
        with st.form("form_login_admin"):
            senha = st.text_input("Senha de acesso:", type="password")
            btn_entrar = st.form_submit_button("Entrar no Painel")
            
            if btn_entrar:
                if senha == "12345":
                    st.session_state['autenticado'] = True
                    st.success("Acesso liberado!")
                    st.rerun()
                else:
                    st.error("Senha incorreta!")
    else:
        # Cabeçalho com botão para sair
        col_header1, col_header2 = st.columns([4, 1])
        with col_header1:
            st.success("Bem-vinda de volta!")
        with col_header2:
            if st.button("🚪 Sair"):
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
        # ABA 1: Agendamentos Recebidos (Firebase Firestore)
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

                st.markdown("<hr style='border: 0.5px solid #fce4ec; margin: 15px 0;'>", unsafe_allow_html=True)
                
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

                st.markdown("<hr style='border: 0.5px solid #fce4ec; margin: 15px 0;'>", unsafe_allow_html=True)
                st.write("#### ⚙️ Alterar Status ou Deletar Registros")
                
                c_id, c_status, c_btn1, c_btn2 = st.columns([2, 1.5, 1, 1])
                
                with c_id:
                    id_selecionado = st.selectbox("Selecione o ID do Agendamento:", df_agendamentos['id'].tolist())
                with c_status:
                    novo_status = st.selectbox("Novo Status:", ["Pendente", "Confirmado", "Concluído", "Cancelado"])
                with c_btn1:
                    st.write(" ")
                    if st.button("Atualizar"):
                        atualizar_status_fn(id_selecionado, novo_status)
                        st.success("Status atualizado com sucesso!")
                        st.rerun()
                with c_btn2:
                    st.write(" ")
                    if st.button("🗑️ Excluir"):
                        deletar_agendamento_fn(id_selecionado)
                        st.warning("Agendamento removido!")
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
                
                if st.form_submit_button("Salvar Trança"):
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
        # ABA 3: Gerenciar Horários de Expediente
        # -----------------------------------------------------------
        with tab3:
            st.write("### 📅 Gerenciar Horários Livres")
            with st.form("form_horarios_livres"):
                data_trabalho = st.date_input("Data do Expediente")
                horarios = st.text_input("Horários disponíveis (separados por vírgula)", value="08:00, 13:00, 17:00")
                
                if st.form_submit_button("Atualizar Agenda"):
                    lista_horarios = [h.strip() for h in horarios.split(",") if h.strip()]
                    db.collection("agenda").document(str(data_trabalho)).set({
                        "data": str(data_trabalho),
                        "horarios_disponiveis": lista_horarios
                    })
                    st.success(f"Agenda para {data_trabalho} atualizada com sucesso!")

    # Fechamento do card branco
    st.markdown('</div>', unsafe_allow_html=True)