import streamlit as st
import pandas as pd
from datetime import datetime, date
import firebase_admin
from firebase_admin import credentials, firestore
from views.admin import render as render_admin

# ==========================================
# 0. INICIALIZAÇÃO E CONEXÃO COM O FIREBASE
# ==========================================
@st.cache_resource
def inicializar_firebase():
    """Inicializa o Firebase usando a chave já configurada no st.secrets['firebase']."""
    if not firebase_admin._apps:
        firebase_secrets = dict(st.secrets["firebase"])
        if "private_key" in firebase_secrets:
            firebase_secrets["private_key"] = firebase_secrets["private_key"].replace("\\n", "\n")

        cred = credentials.Certificate(firebase_secrets)
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

# Instância global do banco de dados
db = inicializar_firebase()


# ==========================================
# FUNÇÕES CRUD DO FIRESTORE
# ==========================================
def carregar_agendamentos():
    """Busca os agendamentos cadastrados na coleção 'agendamentos'."""
    try:
        colecao = db.collection("agendamentos").stream()
        dados = []
        for doc in colecao:
            item = doc.to_dict()
            item["id"] = doc.id
            dados.append(item)
        
        if dados:
            df = pd.DataFrame(dados)
            colunas_desejadas = ["id", "cliente_nome", "cliente_telefone", "servico", "data_agendamento", "horario", "status", "criado_em"]
            colunas_existentes = [col for col in colunas_desejadas if col in df.columns]
            return df[colunas_existentes]
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao conectar com o Firebase: {e}")
        return pd.DataFrame()

def salvar_agendamento(nome, telefone, servico, data_agend, horario):
    """Insere um novo agendamento feito pelo cliente."""
    novo_registro = {
        "cliente_nome": nome,
        "cliente_telefone": telefone,
        "servico": servico,
        "data_agendamento": str(data_agend),
        "horario": horario,
        "status": "Pendente",
        "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    db.collection("agendamentos").add(novo_registro)

def atualizar_status_agendamento(doc_id, novo_status):
    """Atualiza o status no Firebase."""
    db.collection("agendamentos").document(doc_id).update({"status": novo_status})

def deletar_agendamento(doc_id):
    """Remove o documento do Firebase."""
    db.collection("agendamentos").document(doc_id).delete()


# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Paty Tranças | Penteados Afro & Agendamento",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# 2. CSS CUSTOMIZADO
# ==========================================
st.markdown("""
    <style>
    .stAppViewMainTarget { padding-top: 0rem !important; }
    .stMainBlockContainer, div[data-testid="stAppViewBlockContainer"] {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }

    .stApp {
        background-color: #fdf5f8;
        background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%23000000' stroke-width='1.8' stroke-opacity='0.15' stroke-linecap='round'%3E%3Cpath d='M 12 0 C 22 10, 30 20, 25 30 C 20 40, 12 45, 12 50 C 22 60, 30 70, 25 80 C 20 90, 12 95, 12 100' /%3E%3Cpath d='M 15 0 C 25 10, 33 20, 28 30 C 23 40, 15 45, 15 50 C 25 60, 33 70, 28 80 C 23 90, 15 95, 15 100' /%3E%3Cpath d='M 38 0 C 28 10, 20 20, 25 30 C 30 40, 38 45, 38 50 C 28 60, 20 70, 25 80 C 30 90, 38 95, 38 100' /%3E%3Cpath d='M 35 0 C 25 10, 17 20, 22 30 C 27 40, 35 45, 35 50 C 25 60, 17 70, 22 80 C 27 90, 35 95, 35 100' /%3E%3Cpath d='M 62 0 C 72 10, 80 20, 75 30 C 70 40, 62 45, 62 50 C 72 60, 80 70, 75 80 C 70 90, 62 95, 62 100' /%3E%3Cpath d='M 65 0 C 75 10, 83 20, 78 30 C 73 40, 65 45, 65 50 C 75 60, 83 70, 78 80 C 73 90, 65 95, 65 100' /%3E%3Cpath d='M 88 0 C 78 10, 70 20, 75 30 C 80 40, 88 45, 88 50 C 78 60, 70 70, 75 80 C 80 90, 88 95, 88 100' /%3E%3Cpath d='M 85 0 C 75 10, 67 20, 72 30 C 77 40, 85 45, 85 50 C 75 60, 67 70, 72 80 C 77 90, 85 95, 85 100' /%3E%3C/g%3E%3C/svg%3E");
        background-size: 100px 100px;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

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
        margin-bottom: 8px !important;
        margin-top: 0px !important;
        line-height: 1.1 !important;
    }
    
    .subtitle-badge {
        display: inline-block;
        background-color: #ffffff;
        color: #e05297;
        border: 2px solid #f2c4ce;
        border-radius: 16px;
        padding: 6px 16px;
        font-weight: 600;
        font-size: 0.85rem;
        box-shadow: 0px 4px 12px rgba(224, 82, 151, 0.12);
        margin-top: 2px;
        margin-bottom: 5px;
    }

    div.stButton > button {
        width: 100% !important;
        background-color: #ffffff;
        color: #e05297;
        border: 2px solid #f2c4ce;
        border-radius: 16px;
        padding: 6px 4px;
        font-weight: 600;
        font-size: 0.8rem;
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

    .content-card {
        background-color: rgba(255, 255, 255, 0.96);
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #fce4ec;
        margin-top: 5px;
    }

    .custom-footer {
        background-color: rgba(255, 255, 255, 0.92);
        border: 1px solid #fce4ec;
        border-radius: 16px;
        padding: 12px;
        text-align: center;
        margin-top: 25px;
        font-size: 0.8rem;
        color: #666;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.03);
    }

    @media screen and (max-width: 768px) {
        .stMainBlockContainer, div[data-testid="stAppViewBlockContainer"] { padding-top: 0.5rem !important; }
        .top-header h1 { font-size: 1.3rem !important; }
        .subtitle-badge {
            font-size: 0.72rem !important;
            padding: 5px 10px !important;
            border-radius: 12px !important;
            border-width: 1px !important;
        }
        [data-testid="stHorizontalBlock"], div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            justify-content: space-between !important;
            overflow: hidden !important;
            gap: 2px !important;
            width: 100% !important;
            padding: 0 !important;
        }
        [data-testid="column"], div[data-testid="column"], div[data-testid="stColumn"] {
            flex: 1 1 0 !important;
            min-width: 0 !important;
            width: 16.6% !important;
        }
        div.stButton { width: 100% !important; }
        div.stButton > button {
            padding: 5px 1px !important;
            font-size: 0.58rem !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            border-width: 1px !important;
            height: auto !important;
            min-height: 42px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 3. BANNER PRINCIPAL
# ==========================================
st.markdown("""
    <div class="top-header">
        <h1>👑 Paty Tranças</h1>
        <div class="subtitle-badge">
            Especialista em Tranças Afro, Nagô e Penteados Exclusivos
        </div>
    </div>
""", unsafe_allow_html=True)


# ==========================================
# 4. MENU DE NAVEGAÇÃO
# ==========================================
if "pagina_atual" not in st.session_state:
    st.session_state["pagina_atual"] = "📖 Catálogo"

col1, col2, col3, col4, col5, col6 = st.columns(6)

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
    if st.button("📍\nLocal", use_container_width=True):
        st.session_state["pagina_atual"] = "📍 Localização"

with col6:
    if st.button("🔒\nAdmin", use_container_width=True):
        st.session_state["pagina_atual"] = "🔒 Área Administrativa"

st.markdown("<hr style='border: 1px solid #f2c4ce; margin-top: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)


# ==========================================
# 5. RENDERIZAÇÃO DAS PÁGINAS
# ==========================================
pagina = st.session_state["pagina_atual"]

if pagina == "📖 Catálogo":
    st.markdown("""
        <div class="content-card">
            <h3 style="color: #e05297; margin-bottom: 5px;">📖 Catálogo de Estilos & Preços</h3>
            <p style="color: #666; font-size: 0.9rem;">Modelos disponíveis, valores base e estimativa de tempo.</p>
        </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# 🗓️ PÁGINA DE AGENDAMENTO (INTEGRADA AO FIREBASE)
# ------------------------------------------
elif pagina == "🗓️ Agendar":
    st.markdown("""
        <div class="content-card">
            <h3 style="color: #e05297; margin-bottom: 5px;">🗓️ Agende seu Horário</h3>
            <p style="color: #666; font-size: 0.9rem;">Preencha os dados abaixo para enviar sua solicitação de agendamento.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")

    with st.form("form_agendamento_cliente"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nome_cliente = st.text_input("Seu Nome Completo:")
            servico_escolhido = st.selectbox("Escolha o Estilo de Trança:", [
                "Tranças Box Braids",
                "Nagô Desenhada / Lateral",
                "Goddess Braids / Bohemian",
                "Gypsy Braids",
                "Fulani Braids",
                "Entrelace / Crochet Braids",
                "Outro / Atendimento Personalizado"
            ])
        with col_f2:
            telefone_cliente = st.text_input("Seu WhatsApp / Telefone:", placeholder="(19) 99999-9999")
            
            c_d, c_h = st.columns(2)
            with c_d:
                data_atendimento = st.date_input("Data do Atendimento:", min_value=date.today())
            with c_h:
                horario_atendimento = st.selectbox("Horário:", ["08:00", "09:00", "10:30", "13:00", "14:30", "16:00"])

        btn_enviar = st.form_submit_button("✨ Confirmar Solicitação de Agendamento")

        if btn_enviar:
            if not nome_cliente or not telefone_cliente:
                st.error("Por favor, preencha o Nome e o WhatsApp para contato!")
            else:
                salvar_agendamento(nome_cliente, telefone_cliente, servico_escolhido, data_atendimento, horario_atendimento)
                st.success(f"Obrigado, {nome_cliente}! Seu agendamento foi registrado com sucesso. Entraremos em contato via WhatsApp!")

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

elif pagina == "📍 Localização":
    st.markdown("""
        <div class="content-card">
            <h3 style="color: #e05297; margin-bottom: 5px;">📍 Nosso Endereço & Como Chegar</h3>
            <p style="color: #666; font-size: 0.9rem;">Venha conhecer o nosso espaço de atendimento!</p>
        </div>
    """, unsafe_allow_html=True)

elif pagina == "🔒 Área Administrativa":
    render_admin(
        db=db, 
        carregar_agendamentos_fn=carregar_agendamentos, 
        atualizar_status_fn=atualizar_status_agendamento, 
        deletar_agendamento_fn=deletar_agendamento
    )
# ==========================================
# 6. RODAPÉ FIXO
# ==========================================
st.markdown("""
    <div class="custom-footer">
        👑 <b>Paty Tranças</b> • Rua Exemplo das Tranças, 123 - Campinas/SP<br>
        <span style="color: #e05297;">Atendimento com hora marcada</span>
    </div>
""", unsafe_allow_html=True)