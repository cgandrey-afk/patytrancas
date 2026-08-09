import streamlit as st

# 1. Configuração Inicial da Página
st.set_page_config(
    page_title="Paty Tranças | Penteados Afro & Agendamento",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS Customizado Com Padrão de Trança Definido no Fundo
st.markdown("""
    <style>
    /* ELIMINA O ESPAÇO EM BRANCO NATIVO NO TOPO */
    .stAppViewMainTarget {
        padding-top: 0rem !important;
    }
    .stMainBlockContainer, 
    div[data-testid="stAppViewBlockContainer"] {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }

    /* 🎨 FUNDO ROSA COM ESTAMPA ILUSTRADA DE TRANÇAS (GOMINHOS TRANÇADOS) */
    .stApp {
        background-color: #fdf5f8;
        /* Ilustração SVG de gominhos de trança entrelaçados em marca d'água rosa */
        background-image: url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%23e05297' stroke-width='1.5' stroke-opacity='0.18'%3E%3C!-- Gominhos de Trança 1 --%3E%3Cpath d='M20 0 C10 10, 10 20, 20 30 C30 20, 30 10, 20 0 Z'/%3E%3Cpath d='M20 20 C10 30, 10 40, 20 50 C30 40, 30 30, 20 20 Z'/%3E%3Cpath d='M20 40 C10 50, 10 60, 20 70 C30 60, 30 50, 20 40 Z'/%3E%3Cpath d='M20 60 C10 70, 10 80, 20 90 C30 80, 30 70, 20 60 Z'/%3E%3C!-- Gominhos de Trança 2 (Paralelos) --%3E%3Cpath d='M60 0 C50 10, 50 20, 60 30 C70 20, 70 10, 60 0 Z'/%3E%3Cpath d='M60 20 C50 30, 50 40, 60 50 C70 40, 70 30, 60 20 Z'/%3E%3Cpath d='M60 40 C50 50, 50 60, 60 70 C70 60, 70 50, 60 40 Z'/%3E%3Cpath d='M60 60 C50 70, 50 80, 60 90 C70 80, 70 70, 60 60 Z'/%3E%3C/g%3E%3C/svg%3E");
        background-size: 80px 80px;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Banner / Header Principal */
    .top-header {
        text-align: center;
        padding: 0px 0 8px 0 !important;
        margin-top: -10px !important;
    }
    .top-header h1 {
        background: linear-gradient(45deg, #e05297, #9b51e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        margin-bottom: 0px !important;
        margin-top: 0px !important;
        line-height: 1.1 !important;
    }
    .top-header p {
        color: #7d6b7d;
        font-style: italic;
        margin-top: 2px !important;
        margin-bottom: 5px !important;
    }

    /* ESTILO PADRÃO DOS BOTÕES */
    div.stButton > button {
        width: 100% !important;
        background-color: #ffffff;
        color: #e05297;
        border: 2px solid #f2c4ce;
        border-radius: 16px;
        padding: 6px 5px;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 12px rgba(224, 82, 151, 0.12);
        text-align: center !important;
        line-height: 1.2 !important;
        white-space: pre-wrap !important;
    }

    div.stButton > button:hover {
        background-color: #e05297;
        color: #ffffff;
        border-color: #e05297;
        transform: translateY(-2px);
    }

    /* Cartões de Conteúdo Nítidos */
    .content-card {
        background-color: rgba(255, 255, 255, 0.96);
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #fce4ec;
        margin-top: 5px;
    }

    /* --- RESPONSIVO CELULAR --- */
    @media screen and (max-width: 768px) {
        .stMainBlockContainer, 
        div[data-testid="stAppViewBlockContainer"] {
            padding-top: 0.5rem !important;
        }

        .top-header h1 {
            font-size: 1.3rem !important;
        }
        .top-header p {
            font-size: 0.72rem !important;
        }

        [data-testid="stHorizontalBlock"],
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            justify-content: space-between !important;
            overflow: hidden !important;
            gap: 2px !important;
            width: 100% !important;
            padding: 0 !important;
        }

        [data-testid="column"],
        div[data-testid="column"],
        div[data-testid="stColumn"] {
            flex: 1 1 0 !important;
            min-width: 0 !important;
            width: 20% !important;
        }

        div.stButton {
            width: 100% !important;
        }
        div.stButton > button {
            padding: 5px 2px !important;
            font-size: 0.65rem !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            border-width: 1px !important;
            height: auto !important;
            min-height: 40px !important;
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

# 5. Menu Superior Padronizado
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📖\nCatálogo", use_container_width=True):
        st.session_state["pagina_atual"] = "📖 Catálogo"

with col2:
    if st.button("🗓️\nAgendar", use_container_width=True):
        st.session_state["pagina_atual"] = "🗓️ Agendar"

with col3:
    if st.button("📸\nCom IA", use_container_width=True):
        st.session_state["pagina_atual"] = "📸 Trança com IA"

with col4:
    if st.button("🖼️\nGaleria", use_container_width=True):
        st.session_state["pagina_atual"] = "🖼️ Meus Trabalhos"

with col5:
    if st.button("🔒\nAdmin", use_container_width=True):
        st.session_state["pagina_atual"] = "🔒 Área Administrativa"

st.markdown("<hr style='border: 1px solid #f2c4ce; margin-top: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)

# 6. Renderização das Páginas
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