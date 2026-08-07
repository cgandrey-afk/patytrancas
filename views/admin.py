import streamlit as st

def render():
    st.title("🔒 Área Administrativa")

    if 'autenticado' not in st.session_state:
        st.session_state['autenticado'] = False

    if not st.session_state['autenticado']:
        st.subheader("Login de Acesso")
        senha = st.text_input("Senha de acesso", type="password")
        if st.button("Entrar"):
            # Exemplo simples de senha (posteriormente integrado ao Firebase Auth)
            if senha == "12345":
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Senha incorreta!")
    else:
        st.success("Bem-vinda de volta!")
        if st.button("Sair"):
            st.session_state['autenticado'] = False
            st.rerun()

        tab1, tab2 = st.tabs(["➕ Cadastrar Trança", "📅 Agenda & Horários"])
        
        with tab1:
            st.write("### Novo Modelo de Trança")
            nome = st.text_input("Nome do Modelo")
            tempo = st.number_input("Tempo Padrão (em minutos)", step=30, value=180)
            preco = st.text_input("Preço Estimado (ex: R$ 150,00)")
            imagem = st.file_uploader("Foto da Trança", type=["jpg", "png"])
            
            if st.button("Salvar Trança"):
                st.success(f"Modelo '{nome}' cadastrado com sucesso!")

        with tab2:
            st.write("### Gerenciar Horários Livres")
            data_trabalho = st.date_input("Data do Expediente")
            horarios = st.text_input("Horários disponíveis (separados por vírgula)", value="08:00, 13:00, 17:00")
            if st.button("Atualizar Agenda"):
                st.success("Agenda atualizada!")