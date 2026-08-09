import streamlit as st

# 1. Configuração Inicial da Página
st.set_page_config(
    page_title="Paty Tranças | Penteados Afro & Agendamento",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed" # Esconde a barra lateral por padrão
)

# 2. CSS Customizado para Estilização Feminina e Menu No Topo
st.markdown("""
    <style>
    /* Estilização Geral do Fundo */
    .stApp {
        background: linear-gradient(135deg, #fdf7f9 0%, #f7e8ed 100%);
        font-family: 'Poppins', sans-serif;
    }

    /* Esconde elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Topbar / Cabeçalho Principal */
    .top-header {
        text-align: center;
        padding: 20px 0 10px 0;
    }
    .top-header h1 {
        color: #8a2be2;
        background: linear-gradient(45deg, #e05297, #9b51e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.8rem;
        margin-bottom: 5px;
    }
    .top-header p {
        color: #7d6b7d;
        font-size: 1.1rem;
        font-style: italic;
    }

    /* Estilo dos Botões do Menu Superior */
    div.stButton > button {
        width: 100%;
        background-color: #ffffff;
        color: #e05297;
        border: 2px solid #f2c4ce;
        border-radius: 25px;
        padding: 10px 15px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 10px rgba(224, 82, 151, 0.08);
    }

    /* Efeito Hover nos Botões */
    div.stButton > button:hover {
        background-color: #e05297;
        color: #ffffff;
        border-color: #e05297;
        transform: translateY(-2px);
        box-shadow: 0px 6px 15px rgba(224, 82, 151, 0.25);
    }

    /* Destaque para o Botão Selecionado */
    div.stButton > button:focus {
        background-color: #e05297 !important;
        color: #ffffff !important;
        border-color: #e05297 !important;
        box-shadow: 0px 6px 15px rgba(224, 82, 151, 0.3) !important;
    }

    /* Cards de Conteúdo */
    .content-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.04);
        border: 1px solid #fce4ec;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Cabeçalho / Banner do Site
st.markdown("""
    <div class="top-header">
        <h1>👑 Paty Tranças</h1>
        <p>Especialista em Tranças Afro, Nagô e Penteados Exclusivos</p>
    </div>
""", unsafe_allow_html=True)

# 4. Controle de Estado da Página Navegada
if "pagina_atual" not in st.session_state:
    st.session_state["pagina_atual"] = "📖 Catálogo"

# 5. Menu Superior (Colunas no topo da tela)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📖 Catálogo", use_container_width=True):
        st.session_state["pagina_atual"] = "📖 Catálogo"

with col2:
    if st.button("🗓️ Agendar", use_container_width=True):
        st.session_state["pagina_atual"] = "🗓️ Agendar"

with col3:
    if st.button("📸 Trança com IA", use_container_width=True):
        st.session_state["pagina_atual"] = "📸 Trança com IA"

with col4:
    if st.button("🖼️ Meus Trabalhos", use_container_width=True):
        st.session_state["pagina_atual"] = "🖼️ Meus Trabalhos"

with col5:
    if st.button("🔒 Admin", use_container_width=True):
        st.session_state["pagina_atual"] = "🔒 Área Administrativa"

st.markdown("<hr style='border: 1px solid #f2c4ce; margin-top: 15px; margin-bottom: 25px;'>", unsafe_allow_html=True)

# 6. Renderização do Conteúdo de Acordo com a Página Selecionada
pagina = st.session_state["pagina_atual"]

if pagina == "📖 Catálogo":
    st.markdown("""
        <div class="content-card">
            <h2 style="color: #e05297;">📖 Catálogo de Estilos & Valores Base</h2>
            <p style="color: #666;">Escolha o estilo ideal para você. Confira nossos valores e tempo médio de execução.</p>
        </div>
    """, unsafe_allow_html=True)
    # [Futuro: Aqui vamos carregar os cards do catálogo do banco de dados]

elif pagina == "🗓️ Agendar":
    st.markdown("""
        <div class="content-card">
            <h2 style="color: #e05297;">🗓️ Agende seu Horário</h2>
            <p style="color: #666;">Preencha seus dados, selecione o estilo desejado e escolha a melhor data no calendário.</p>
        </div>
    """, unsafe_allow_html=True)
    # [Futuro: Formulário de agendamento]

elif pagina == "📸 Trança com IA":
    st.markdown("""
        <div class="content-card">
            <h2 style="color: #e05297;">📸 Avaliação Personalizada com Inteligência Artificial</h2>
            <p style="color: #666;">Envie uma foto de inspiração da trança e do seu cabelo para calcularmos a duração exata!</p>
        </div>
    """, unsafe_allow_html=True)
    # [Aqui chamaremos a função de análise de imagem com Gemini]

elif pagina == "🖼️ Meus Trabalhos":
    st.markdown("""
        <div class="content-card">
            <h2 style="color: #e05297;">🖼️ Galeria & Portfólio de Clientes</h2>
            <p style="color: #666;">Confira a qualidade dos acabamentos e fotos reais dos penteados realizados no estúdio.</p>
        </div>
    """, unsafe_allow_html=True)
    # [Futuro: Mural estilo Instagram com fotos reais dos trabalhos]

elif pagina == "🔒 Área Administrativa":
    st.markdown("""
        <div class="content-card">
            <h2 style="color: #e05297;">🔒 Painel de Controle da Trancista</h2>
            <p style="color: #666;">Gestão de agendamentos, cadastro de fotos no portfólio e configuração do catálogo.</p>
        </div>
    """, unsafe_allow_html=True)
    # [Futuro: Login e gestão do sistema]