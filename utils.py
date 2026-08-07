import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from PIL import Image
import json
import io

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
        # 1. Configura a chave de API
        api_key = st.secrets["gemini"]["api_key"]
        genai.configure(api_key=api_key)
        
        # 2. Reseta o ponteiro e lê os bytes da imagem
        imagem_upload.seek(0)
        bytes_imagem = imagem_upload.read()
        imagem_pil = Image.open(io.BytesIO(bytes_imagem))
        
        prompt = """
        Você é um especialista em penteados e tranças afro.
        Analise a imagem enviada e estime a complexidade e o tempo necessário para executar o penteado.
        
        Retorne ESTRITAMENTE um JSON no formato abaixo, sem nenhum texto antes ou depois:
        {
          "estilo_identificado": "Nome do modelo de trança identificado",
          "dificuldade": "Média",
          "tempo_estimado_minutos": 180,
          "observacao": "Uma breve explicação sobre a densidade ou tamanho que influenciou o tempo estimado."
        }
        """

        # 3. Desativa filtros de bloqueio indevidos para fotos de rostos/cabelo
        safety_settings = [
            {
                "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
                "threshold": HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                "threshold": HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                "threshold": HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                "threshold": HarmBlockThreshold.BLOCK_NONE,
            },
        ]

        modelos_tentativa = [
            'gemini-1.5-flash',
            'models/gemini-1.5-flash',
            'gemini-1.5-pro',
            'models/gemini-1.5-pro'
        ]

        texto_resultado = None
        ultimo_erro = None

        for nome_modelo in modelos_tentativa:
            try:
                model = genai.GenerativeModel(model_name=nome_modelo)
                response = model.generate_content(
                    [prompt, imagem_pil],
                    safety_settings=safety_settings
                )
                
                # Tenta capturar o texto direto dos candidatos
                if response and response.candidates:
                    cand = response.candidates[0]
                    if cand.content and cand.content.parts:
                        texto_resultado = cand.content.parts[0].text
                        if texto_resultado and texto_resultado.strip():
                            break
            except Exception as err:
                ultimo_erro = err
                continue

        if not texto_resultado or not texto_resultado.strip():
            raise Exception(f"A API respondeu sem conteúdo. Verifique a imagem ou tente outra foto. Detalhes: {ultimo_erro}")

        texto_limpo = texto_resultado.strip()
        
        # Limpa marcadores de código caso o Gemini envie ```json ... ```
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