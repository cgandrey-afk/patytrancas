import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------------------------------------------------------
# Módulos do Firebase (Importe as funções do seu arquivo principal ou helper)
# Exemplo: import firebase_admin / firestore de onde estiver configurado
# -------------------------------------------------------------------

def render(db, carregar_agendamentos_fn, atualizar_status_fn, deletar_agendamento_fn):
    # Envolve todo o conteúdo do Admin no card de fundo branco
    st.markdown("""
        <div class="content-card">
            <h2 style="color: #e05297; margin-bottom: 5px;">🔒 Área Administrativa</h2>
            <p style="color: #555; font-size: 0.9rem;">Gerencie o catálogo de tranças, a agenda e os agendamentos do estúdio.</p>
            <hr style="border: 0.5px solid #fce4ec; margin: 12px 0;">
    """, unsafe_allow_html=True)

    # Controle de Sessão / Autenticação
    if 'autenticado' not in st.session_state:
        st.session_state['autenticado'] = False

    if not st.session_state['autenticado']:
        st.subheader("🔑 Login de Acesso")
        with st.form("form_login_admin"):
            senha = st.text_input("Senha de acesso:", type="password")
            btn_entrar = st.form_submit_button("Entrar no Painel")
            
            if btn_entrar:
                # Altere a senha se necessário (padrão 12345)
                if senha == "12345":
                    st.session_state['autenticado'] = True
                    st.success("Acesso liberado!")
                    st.rerun()
                else:
                    st.error("Senha incorreta!")
    else:
        # Cabeçalho com botão de saída
        col_header1, col_header2 = st.columns([4, 1])
        with col_header1:
            st.success("Bem-vinda de volta, Paty!")
        with col_header2:
            if st.button("🚪 Sair"):
                st.session_state['autenticado'] = False
                st.rerun()

        st.write("") # Espaçamento

        # Abas de Gerenciamento
        tab_agendamentos, tab_cadastrar, tab_agenda = st.tabs([
            "📋 Agendamentos Recebidos", 
            "➕ Cadastrar Trança", 
            "📅 Agenda & Horários"
        ])

        # -----------------------------------------------------------
        # ABA 1: Agendamentos do Firebase
        # -----------------------------------------------------------
        with tab_agendamentos:
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
                st.write("#### ⚙️ Gerenciar Agendamento Selecionado")
                
                c_id, c_status, c_btn1, c_btn2 = st.columns([2, 1.5, 1, 1])
                
                with c_id:
                    id_selecionado = st.selectbox("Selecione o ID:", df_agendamentos['id'].tolist())
                with c_status:
                    novo_status = st.selectbox("Novo Status:", ["Pendente", "Confirmado", "Concluído", "Cancelado"])
                with c_btn1:
                    st.write(" ")
                    if st.button("Atualizar"):
                        atualizar_status_fn(id_selecionado, novo_status)
                        st.success("Status atualizado!")
                        st.rerun()
                with c_btn2:
                    st.write(" ")
                    if st.button("🗑️ Excluir"):
                        deletar_agendamento_fn(id_selecionado)
                        st.warning("Agendamento excluído!")
                        st.rerun()
            else:
                st.info("Nenhum agendamento encontrado no Firebase.")

        # -----------------------------------------------------------
        # ABA 2: Novo Modelo de Trança (Salvar no Firebase / Catálogo)
        # -----------------------------------------------------------
        with tab_cadastrar:
            st.write("### ➕ Adicionar Modelo ao Catálogo")
            with st.form("form_nova_tranca"):
                nome_tranca = st.text_input("Nome do Modelo")
                tempo = st.number_input("Tempo Padrão (em minutos)", step=30, value=180)
                preco = st.text_input("Preço Estimado (ex: R$ 150,00)")
                imagem = st.file_uploader("Foto da Trança", type=["jpg", "jpeg", "png"])
                
                btn_salvar_tranca = st.form_submit_button("Salvar Trança no Banco")
                
                if btn_salvar_tranca:
                    if nome_tranca and preco:
                        # Salva a nova trança diretamente na coleção 'catalogo' do Firebase
                        doc_ref = db.collection("catalogo").document()
                        doc_ref.set({
                            "nome": nome_tranca,
                            "tempo_minutos": tempo,
                            "preco": preco,
                            "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                        st.success(f"Modelo '{nome_tranca}' salvo com sucesso no Firebase!")
                    else:
                        st.error("Por favor, preencha o Nome e o Preço do modelo.")

        # -----------------------------------------------------------
        # ABA 3: Gerenciar Horários Livres (Configuração de Agenda)
        # -----------------------------------------------------------
        with tab_agenda:
            st.write("### 📅 Configurar Horários Disponíveis")
            with st.form("form_agenda_horarios"):
                data_trabalho = st.date_input("Data do Expediente")
                horarios = st.text_input("Horários disponíveis (separados por vírgula)", value="08:00, 13:00, 17:00")
                btn_salvar_agenda = st.form_submit_button("Atualizar Agenda no Firebase")
                
                if btn_salvar_agenda:
                    # Salva os horários liberados para determinado dia na coleção 'agenda'
                    lista_horarios = [h.strip() for h in horarios.split(",") if h.strip()]
                    db.collection("agenda").document(str(data_trabalho)).set({
                        "data": str(data_trabalho),
                        "horarios_disponiveis": lista_horarios
                    })
                    st.success(f"Agenda para o dia {data_trabalho} atualizada com sucesso!")

    # Fecha o div do fundo branco
    st.markdown("</div>", unsafe_allow_html=True)