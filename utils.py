import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

def formatar_tempo(minutos):
    """Formata minutos no formato legível de horas e minutos."""
    horas = minutos // 60
    min_restantes = minutos % 60
    if horas > 0 and min_restantes > 0:
        return f"{horas}h {min_restantes}min"
    elif horas > 0:
        return f"{horas}h"
    return f"{min_restantes}min"

def analisar_imagem_com_gemini(imagem_upload):
    """Envia a imagem para a API Gemini e retorna a estimativa de tempo e complexidade."""
    try:
        # Recupera a chave salva nas Secrets do Streamlit Cloud
        api_key = st.secrets["gemini"]["api_key"]
        genai.configure(api_key=api_key)
        
        # Carrega a imagem enviada
        imagem = Image.open(imagem_upload)
        
        # Modelo atualizado e estável
        # Caso gemini-2.0-flash não esteja disponível na sua conta, altere para 'gemini-1.5-pro'
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash',
            generation_config={"response_mime_type": "application/json"}
        )
        
        prompt = """
        Você é um especialista em penteados e tranças afro.
        Analise a imagem enviada e estime a complexidade e o tempo necessário para executar o penteado.
        
        Retorne um JSON com a seguinte estrutura:
        {
          "estilo_identificado": "Nome do modelo de trança identificado",
          "dificuldade": "Baixa" ou "Média" ou "Alta" ou "Muito Alta",
          "tempo_estimado_minutos": 180,
          "observacao": "Uma breve explicação sobre a densidade ou tamanho que influenciou o tempo estimado."
        }
        """
        
        response = model.generate_content([prompt, imagem])
        
        # Converte a resposta estruturada em dicionário
        dados = json.loads(response.text)
        return dados
        
    except Exception as e:
        # Fallback caso o modelo 2.0 ainda não esteja ativo na chave
        try:
            model = genai.GenerativeModel(
                model_name='gemini-1.5-pro',
                generation_config={"response_mime_type": "application/json"}
            )
            response = model.generate_content([prompt, imagem])
            return json.loads(response.text)
        except Exception as err_fallback:
            st.error(f"Erro ao analisar imagem com IA: {err_fallback}")
            return None