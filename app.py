import streamlit as st

# 1. Configuração Inicial da Página
st.set_page_config(
    page_title="Paty Tranças | Penteados Afro & Agendamento",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS Customizado para Telas Pequenas e Ultra Pequenas (Celulares)
st.markdown("""
    <style>
    /* Estilização Geral do Fundo */
    .stApp {
        background: linear-gradient(135deg, #fdf7f9 0%, #f7e8ed 100%);
        font-family: 'Poppins', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Banner / Header Principal */
    .top-header {
        text-align: center;
        padding: 10px 0;
    }
    .top-header h1 {
        background: linear-gradient(45deg, #e05297, #9b51e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        margin-bottom: 2px;
    }
    .top-header p {
        color: #7d6b7d;
        font-style: italic;
    }

    /* --- ESTILO PADRÃO DOS BOTÕES (DESKTOP) --- */
    div.stButton > button {
        width: 100%;
        background-color: #ffffff;
        color: #e05297;
        border: 2px solid #f2c4ce;
        border-radius: 20px;
        padding: 8px 12px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 8px rgba(224, 82, 151, 0.08);
        white-space: nowrap;
    }

    div.stButton > button:hover {
        background-color: #e05297;
        color: #ffffff;
        border-color: #e05297;
        transform: translateY(-2px);
    }

    .content-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.04);
        border: 1px solid #fce4ec;
        margin-top: 10px;
    }

    /* --- REGRA PARA CELULARES E TELAS MUITO PEQUENAS (Abaixo de 768px) --- */
    @media only screen and (max-width: 768px) {
        .top-header h1 {
            font-size: 1.6rem !important;
        }
        .top-header p {
            font-size: 0.8rem !important;
        }
        
        /* Força a barra de botões a virar um container de rolagem horizontal */
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            scroll-behavior: smooth;
            -webkit-overflow-scrolling: touch;
            gap: 6px !important;
            padding-bottom: 8px !important;
        }

        /* Oculta a barra de rolagem nativa feia mantendo a função de deslizar */
        div[data-testid="stHorizontalBlock"]::-webkit-scrollbar {
            height: 3px;
        }
        div[data-testid="stHorizontalBlock"]::-webkit-scrollbar-thumb {
            background: #f2c4ce;
            border-radius: 10px;
        }

        /* Garante tamanho proporcional e compacto em telas estreitas */
        div[data-testid="column"] {
            width: auto !important;
            min-width: max-content !important;
            flex: 0 0 auto !important;
        }

        /* Botões bem compactos para caber na tela pequena */
        div.stButton > button {
            padding: 5px 10px !important;
            font-size: 0.72rem !important;
            border-radius: 12px !important;
            border-width: 1.5px !important;
            min-height: unset !important;
            height: auto !important;
        }

        .content-card {
            padding: 15px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 3. Banner / Cabeçalho
st.markdown("""
    <div class="top-header">
        <h1>👑 Paty Tranças</h1>
        <p>Especialista em Tranças Afro, Nagô e Penteados Exclusivos</p>
    </div>
""", unsafe_allow_html=True)

# 4. Controle de Navegação
if "pagina_atual" not in st.session_state:
    st.session_state["pagina_atual"] = "📖 Catálogo"

# 5. Menu Superior (5 Colunas)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📖 Catálogo", use_container_width=True):
        st.session_state["pagina_atual"] = "📖 Catálogo"

with col2:
    if st.button("🗓️ Agendar", use_container_width=True):
        st.session_state["pagina_atual"] = "🗓️ Agendar"

with col3:
    if st.button("📸 Com IA", use_container_width=True):
        st.session_state["pagina_atual"] = "📸 Trança com IA"

with col4:
    if st.button("🖼️ Trabalhos", use_container_width=True):
        st.session_state["pagina_atual"] = "🖼️ Meus Trabalhos"

with col5:
    if st.button("🔒 Admin", use_container_width=True):
        st.session_state["pagina_atual"] = "🔒 Área Administrativa"

st.markdown("<hr style='border: 1px solid #f2c4ce; margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)

# 6. Renderização de Páginas
pagina = st.session_state["pagina_atual"]

if pagina == "📖 Catálogo":
    st.markdown("""
        <div class="content-card">
            <h3 style="color: #e05297; margin-bottom: 5px;">📖 Catálogo de Estilos & Preços</h3>
            <p style="color: #666; font-size: 0.9rem;">Modelos disponíveis, valores base e estimativa de tempo.</p>
        </div>
    """, unsafe_allow_html=True)

elif pagina == "🗓️ Agendar":
    st.markdown("""
        <div class="content-card">
            <h3 style="color: #e05297; margin-bottom: 5px;">🗓️ Agende seu Horário</h3>
            <p style="color: #666; font-size: 0.9rem;">Escolha o modelo, a melhor data e horário para atendimento.</p>
        </div>
    """, unsafe_allow_html=True)

elif pagina == "📸 Trança com IA":
    st.markdown("""
        <div class="content-card">
            <h3 style="color: #e05297; margin-bottom: 5px;">📸 Análise com Inteligência Artificial</h3>
            <p style="color: #666; font-size: 0.9rem;">Envie a foto de inspiração para estipular o tempo exato!</p>
        </div>
    """, unsafe_allow_html=True)

elif pagina == "🖼️ Meus Trabalhos":
    st.markdown("""
        <div class="content-card">
            <h3 style="color: #e05297; margin-bottom: 5px;">🖼️ Galeria de Trabalhos Realizados</h3>
            <p style="color: #666; font-size: 0.9rem;">Confira os resultados reais de clientes do estúdio.</p>
        </div>
    """, unsafe_allow_html=True)

elif pagina == "🔒 Área Administrativa":
    st.markdown("""
        <div class="content-card">
            <h3 style="color: #e05297; margin-bottom: 5px;">🔒 Área Administrativa</h3>
            <p style="color: #666; font-size: 0.9rem;">Gerenciamento de agenda, catálogo e configurações.</p>
        </div>
    """, unsafe_allow_html=True)