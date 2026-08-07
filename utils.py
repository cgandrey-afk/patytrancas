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
        
        prompt = """
        Você é um especialista em penteados e tranças afro.
        Analise a imagem enviada e estime a complexidade e o tempo necessário para executar o penteado.
        
        Retorne um JSON com a seguinte estrutura:
        {
          "estilo_identificado": "Nome do modelo de trança identificado",
          "dificuldade": "Baixa",
          "tempo_estimado_minutos": 180,
          "observacao": "Uma breve explicação sobre a densidade ou tamanho que influenciou o tempo estimado."
        }
        """

        # Busca dinamicamente na API do Google quais modelos suportam geração de conteúdo
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

        # Passamos a configuração para a API retornar estritamente JSON puro
        generation_config = genai.GenerationConfig(
            response_mime_type="application/json"
        )

        for nome_modelo in modelos_disponiveis:
            try:
                model = genai.GenerativeModel(
                    model_name=nome_modelo,
                    generation_config=generation_config
                )
                response = model.generate_content([prompt, imagem])
                if response and response.text:
                    break
            except Exception as err:
                ultimo_erro = err
                continue

        if not response or not response.text:
            raise Exception(f"Nenhum modelo retornou resposta válida. Erro: {ultimo_erro}")

        # Como forçamos o response_mime_type em JSON, o response.text já vem 100% limpo
        dados = json.loads(response.text.strip())
        return dados
        
    except Exception as e:
        st.error(f"Erro ao analisar imagem com IA: {e}")
        return None