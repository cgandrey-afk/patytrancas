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
        # 1. Recupera e configura a chave da API
        api_key = st.secrets["gemini"]["api_key"]
        genai.configure(api_key=api_key)
        
        # 2. Processa a imagem para garantir compatibilidade
        imagem_upload.seek(0)
        bytes_imagem = imagem_upload.read()
        imagem_pil = Image.open(io.BytesIO(bytes_imagem))
        
        # Converte para RGB se for RGBA/PNG transparente
        if imagem_pil.mode in ("RGBA", "P"):
            imagem_pil = imagem_pil.convert("RGB")
        
        prompt = """
        Você é um especialista em penteados e tranças afro.
        Analise a imagem enviada e estime a complexidade e o tempo necessário para executar o penteado.
        
        Retorne ESTRITAMENTE um JSON com esta estrutura (sem marcações markdown adicionais fora do JSON):
        {
          "estilo_identificado": "Nome do modelo de trança identificado",
          "dificuldade": "Média",
          "tempo_estimado_minutos": 180,
          "observacao": "Uma breve explicação sobre a densidade ou tamanho que influenciou o tempo estimado."
        }
        """

        # 3. Modelos vigentes na API do Google Gemini
        modelos_tentativa = [
            'gemini-2.5-flash',
            'gemini-2.0-flash',
            'gemini-1.5-flash-latest',
            'gemini-1.5-flash'
        ]

        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        texto_resultado = None
        ultimo_erro = None

        for nome_modelo in modelos_tentativa:
            try:
                model = genai.GenerativeModel(model_name=nome_modelo)
                response = model.generate_content(
                    [prompt, imagem_pil],
                    safety_settings=safety_settings
                )
                
                if response and hasattr(response, 'text') and response.text and response.text.strip():
                    texto_resultado = response.text.strip()
                    break
                elif response and response.candidates:
                    cand = response.candidates[0]
                    if cand.content and cand.content.parts:
                        texto_resultado = cand.content.parts[0].text.strip()
                        if texto_resultado:
                            break
            except Exception as err:
                ultimo_erro = err
                continue

        if not texto_resultado:
            raise Exception(f"Erro ao conectar aos modelos do Gemini. Última tentativa: {ultimo_erro}")

        # Limpa blocos markdown no caso de ```json ... ```
        if texto_resultado.startswith("```"):
            lines = texto_resultado.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            texto_resultado = "\n".join(lines).strip()

        dados = json.loads(texto_resultado)
        return dados
        
    except Exception as e:
        st.error(f"Erro ao analisar imagem com IA: {e}")
        return None