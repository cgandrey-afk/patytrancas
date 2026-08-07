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
        
        Retorne ESTRITAMENTE um JSON no seguinte formato:
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

        # Lista de fallback caso a busca dinâmica falhe
        if not modelos_disponiveis:
            modelos_disponiveis = [
                'models/gemini-1.5-flash-latest',
                'models/gemini-1.5-flash',
                'models/gemini-1.5-pro-latest',
                'models/gemini-1.5-pro',
                'models/gemini-pro'
            ]

        response = None
        ultimo_erro = None

        # Testa os modelos que realmente existem na sua conta
        for nome_modelo in modelos_disponiveis:
            try:
                model = genai.GenerativeModel(nome_modelo)
                response = model.generate_content([prompt, imagem])
                if response and response.text:
                    break
            except Exception as err:
                ultimo_erro = err
                continue

        if not response or not response.text:
            raise Exception(f"Nenhum modelo respondeu. Modelos testados: {modelos_disponiveis}. Erro: {ultimo_erro}")

        texto_limpo = response.text.strip()
        if texto_limpo.startswith("```"):
            lines = texto_limpo.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            texto_limpo = "\n".join(lines).strip()

        dados = json.loads(texto_limpo)
        return dados
        
    except Exception as e:
        st.error(f"Erro ao analisar imagem com IA: {e}")
        return None