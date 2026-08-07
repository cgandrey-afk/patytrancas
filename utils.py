import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
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
        
        prompt = """
        Você é um especialista em penteados e tranças afro.
        Analise a imagem enviada e estime a complexidade e o tempo necessário para executar o penteado.
        
        Retorne ESTRITAMENTE um JSON com esta estrutura (sem formatação markdown adicionais fora do json):
        {
          "estilo_identificado": "Nome do modelo de trança identificado",
          "dificuldade": "Média",
          "tempo_estimado_minutos": 180,
          "observacao": "Uma breve explicação sobre a densidade ou tamanho que influenciou o tempo estimado."
        }
        """

        # Configurações para garantir retorno puro em JSON
        generation_config = genai.GenerationConfig(
            response_mime_type="application/json"
        )

        # Configurações para evitar bloqueio indevido por filtros de imagem
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # Busca dinamicamente os modelos disponíveis
        modelos_disponiveis = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    modelos_disponiveis.append(m.name)
        except Exception:
            pass

        if not modelos_disponiveis:
            modelos_disponiveis = [
                'models/gemini-1.5-flash-latest',
                'models/gemini-1.5-flash',
                'models/gemini-1.5-pro-latest',
                'models/gemini-1.5-pro'
            ]

        response = None
        ultimo_erro = None

        for nome_modelo in modelos_disponiveis:
            try:
                model = genai.GenerativeModel(
                    model_name=nome_modelo,
                    generation_config=generation_config,
                    safety_settings=safety_settings
                )
                response = model.generate_content([prompt, imagem])
                
                # Verifica se o modelo retornou algum texto de fato
                if response and hasattr(response, 'text') and response.text and response.text.strip():
                    break
            except Exception as err:
                ultimo_erro = err
                continue

        if not response or not hasattr(response, 'text') or not response.text or not response.text.strip():
            raise Exception(f"A API do Gemini retornou uma resposta vazia. (Erro/Filtro: {ultimo_erro})")

        texto_resposta = response.text.strip()
        dados = json.loads(texto_resposta)
        return dados
        
    except Exception as e:
        st.error(f"Erro ao analisar imagem com IA: {e}")
        return None