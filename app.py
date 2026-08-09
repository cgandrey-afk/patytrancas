import streamlit as st

# 1. Configuração Inicial da Página
st.set_page_config(
    page_title="Paty Tranças | Penteados Afro & Agendamento",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS Customizado Com Tranças Empilhadas / Encadeadas no Fundo
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

    /* 🎨 FUNDO ROSA COM TRANÇAS CONTINUAS EMPILHADAS (GOMINHO SOBRE GOMINHO) */
    .stApp {
        background-color: #fdf5f8;
        /* SVG formando colunas de tranças com gominhos sobrepostos */
        background-image: url("data:image/svg+xml,%3Csvg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%23e05297' stroke-width='1.6' stroke-opacity='0.22' stroke-linecap='round' stroke-linejoin='round'%3E%3C!-- COLUNA DE TRANÇA 1 (ESQUERDA) --%3E%3C!-- Gomos encadeados e sobrepostos a cada 16px --%3E%3Cpath d='M 30,2 Q 20,10 30,18 Q 40,10 30,2 Z' /%3E%3Cpath d='M 30,14 Q 20,22 30,30 Q 40,22 30,14 Z' /%3E%3Cpath d='M 30,26 Q 20,34 30,42 Q 40,34 30,26 Z' /%3E%3Cpath d='M 30,38 Q 20,46 30,54 Q 40,46 30,38 Z' /%3E%3Cpath d='M 30,50 Q 20,58 30,66 Q 40,58 30,50 Z' /%3E%3Cpath d='M 30,62 Q 20,70 30,78 Q 40,70 30,62 Z' /%3E%3Cpath d='M 30,74 Q 20,82 30,90 Q 40,82 30,74 Z' /%3E%3Cpath d='M 30,86 Q 20,94 30,102 Q 40,94 30,86 Z' /%3E%3Cpath d='M 30,98 Q 20,106 30,114 Q 40,106 30,98 Z' /%3E%3C!-- COLUNA DE TRANÇA 2 (DIREITA) com leve deslocamento --%3E%3Cpath d='M 90,8 Q 80,16 90,24 Q 100,16 90,8 Z' /%3E%3Cpath d='M 90,20 Q 80,28 90,36 Q 100,28 90,20 Z' /%3E%3Cpath d='M 90,32 Q 80,40 90,48 Q 100,40 90,32 Z' /%3E%3Cpath d='M 90,44 Q 80,52 90,60 Q 100,52 90,44 Z' /%3E%3Cpath d='M 90,56 Q 80,64 90,72 Q 100,64 90,56 Z' /%3E%3Cpath d='M 90,68 Q 80,76 90,84 Q 100,76 90,68 Z' /%3E%3Cpath d='M 90,80 Q 80,88 90,96 Q 100,88 90,80 Z' /%3E%3Cpath d='M 90,92 Q 80,100 90,108 Q 100,100 90,92 Z' /%3E%3C/g%3E%3C/svg%3E");
        background-size: 120px 120px;
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

    /* Cartões de Conteúdo */
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