import streamlit as st
import pandas as pd
from datetime import datetime, date
import firebase_admin
from firebase_admin import credentials, firestore
import agendamento
import admin
import utils

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
# 1. CONFIGURAÇÃO DA PÁGINA E CSS
# ==========================================
st.set_page_config(
    page_title="Paty Tranças | Penteados Afro & Agendamento",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Carrega o CSS global centralizado
utils.carregar_css()


# ==========================================
# 2. BANNER PRINCIPAL
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
# 3. MENU DE NAVEGAÇÃO RESPONSIVO
# ==========================================
if "pagina_atual" not in st.session_state:
    st.session_state["pagina_atual"] = "📖 Catálogo"

opcoes_menu = {
    "📖 Catálogo": "📖 Catálogo",
    "🗓️ Agendar": "🗓️ Agendar",
    "📸 Com IA": "📸 Trança com IA",
    "🖼️ Galeria": "🖼️ Meus Trabalhos",
    "📍 Local": "📍 Localização",
    "🔒 Admin": "🔒 Área Administrativa"
}

# --- A. MENU DESKTOP ---
st.markdown('<div class="menu-desktop-container">', unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6 = st.columns(6)

for col, (label, pagina_target) in zip([col1, col2, col3, col4, col5, col6], opcoes_menu.items()):
    with col:
        if st.button(label, key=f"btn_desk_{label}", use_container_width=True):
            st.session_state["pagina_atual"] = pagina_target
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- B. MENU MOBILE ---
st.markdown('<div class="menu-mobile-container">', unsafe_allow_html=True)
with st.expander("≡ MENU DE NAVEGAÇÃO", expanded=False):
    for label, pagina_target in opcoes_menu.items():
        is_active = (st.session_state["pagina_atual"] == pagina_target)
        prefixo = "➔ " if is_active else ""
        
        if st.button(f"{prefixo}{label}", key=f"btn_mob_{label}", use_container_width=True):
            st.session_state["pagina_atual"] = pagina_target
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #f2c4ce; margin-top: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)

# ==========================================
# 4. RENDERIZAÇÃO DAS PÁGINAS
# ==========================================
pagina = st.session_state["pagina_atual"]

if pagina == "📖 Catálogo":
    st.markdown("""
        <div class="content-card">
            <h3 style="color: #e05297; margin-bottom: 5px;">📖 Catálogo de Estilos & Preços</h3>
            <p style="color: #666; font-size: 0.9rem;">Modelos disponíveis, valores base e estimativa de tempo.</p>
        </div>
    """, unsafe_allow_html=True)

elif pagina == "🗓️ Agendar":
    agendamento.render(db=db, salvar_agendamento_fn=salvar_agendamento)

elif pagina == "📸 Trança com IA":
    with st.container(border=True):
        st.markdown('<h3 style="color: #e05297; margin-bottom: 5px;">✨ Estimativa Inteligente de Penteado</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666; font-size: 0.9rem;">Envie uma foto do estilo de trança desejado para nossa IA analisar a complexidade e o tempo estimado de atendimento.</p>', unsafe_allow_html=True)
        st.divider()

        upload_foto = st.file_uploader(
            "Envie a imagem do penteado (JPG, JPEG ou PNG):", 
            type=["jpg", "jpeg", "png"]
        )

        if upload_foto is not None:
            col1, col2 = st.columns([1, 1])

            with col1:
                st.image(upload_foto, caption="Foto enviada", use_container_width=True)

            with col2:
                st.markdown('<div class="botoes-acao">', unsafe_allow_html=True)
                btn_analisar = st.button("🔍 Analisar Penteado com IA", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                if btn_analisar:
                    with st.spinner("Analisando complexidade e estimando o tempo..."):
                        resultado = utils.analisar_imagem_com_gemini(upload_foto)

                    if resultado:
                        st.success("Análise concluída!")
                        st.markdown(f"**Estilo Identificado:** {resultado.get('estilo_identificado', 'N/A')}")
                        st.markdown(f"**Dificuldade:** `{resultado.get('dificuldade', 'N/A')}`")
                        
                        tempo_min = resultado.get('tempo_estimado_minutos', 0)
                        tempo_formatado = utils.formatar_tempo(tempo_min)
                        st.markdown(f"⏱️ **Tempo Estimado:** `{tempo_formatado}`")
                        st.info(f"💡 **Observação da IA:**\n{resultado.get('observacao', '')}")

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
    admin.render(
        db=db, 
        carregar_agendamentos_fn=carregar_agendamentos, 
        atualizar_status_fn=atualizar_status_agendamento, 
        deletar_agendamento_fn=deletar_agendamento
    )

# ==========================================
# 5. RODAPÉ FIXO
# ==========================================
st.markdown("""
    <div class="custom-footer">
        👑 <b>Paty Tranças</b> • Rua Exemplo das Tranças, 123 - Campinas/SP<br>
        <span style="color: #e05297;">Atendimento com hora marcada</span>
    </div>
""", unsafe_allow_html=True)