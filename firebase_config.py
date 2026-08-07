import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

@st.cache_resource
def inicializar_firebase():
    """Inicializa o SDK do Firebase usando os Secrets do Streamlit."""
    if not firebase_admin._apps:
        # Monta o dicionário de credenciais a partir das Secrets
        cred_dict = dict(st.secrets["firebase"])
        
        # Garante a formatação correta das quebras de linha na chave privada
        if "private_key" in cred_dict:
            cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
            
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        
    return firestore.client()

# Instância global do banco de dados
db = inicializar_firebase()

# -------------------------------------------------------------
# FUNÇÕES DE INTERAÇÃO COM O BANCO DE DADOS (FIRESTORE)
# -------------------------------------------------------------

def buscar_trancas():
    """Busca todas as tranças cadastradas no Firestore."""
    trancas_ref = db.collection("trancas").stream()
    lista_trancas = []
    for doc in trancas_ref:
        dado = doc.to_dict()
        dado["id"] = doc.id
        lista_trancas.append(dado)
    return lista_trancas

def cadastrar_tranca(nome, tempo_min, preco, imagem_url=""):
    """Cadastra um novo modelo de trança no Firestore."""
    doc_ref = db.collection("trancas").document()
    doc_ref.set({
        "nome": nome,
        "tempo_min": tempo_min,
        "preco": preco,
        "imagem_url": imagem_url
    })

def buscar_horarios_livres(data_str):
    """Busca os horários disponíveis para uma data específica."""
    doc = db.collection("agenda").document(data_str).get()
    if doc.exists:
        dados = doc.to_dict()
        return dados.get("horarios", [])
    return ["08:00", "13:00", "17:00"] # Padrão caso não tenha sido cadastrado

def salvar_agendamento(dados):
    """Salva um novo agendamento de cliente."""
    db.collection("agendamentos").add(dados)
    return True