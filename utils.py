import streamlit as st
from google import genai
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
        # 1. Recupera a chave salva nas Secrets do Streamlit Cloud
        api_key = st.secrets["gemini"]["api_key"]
        
        # Cria o cliente usando a nova SDK oficial google-genai
        client = genai.Client(api_key=api_key)
        
        # 2. Processa a imagem para garantir compatibilidade
        imagem_upload.seek(0)
        bytes_imagem = imagem_upload.read()
        imagem_pil = Image.open(io.BytesIO(bytes_imagem))
        
        if imagem_pil.mode in ("RGBA", "P"):
            imagem_pil = imagem_pil.convert("RGB")
        
        prompt = """
        Você é um especialista em penteados e tranças afro.
        Analise a imagem enviada e estime a complexidade e o tempo necessário para executar o penteado.
        
        Retorne ESTRITAMENTE um JSON no seguinte formato (sem marcações de markdown adicionais):
        {
          "estilo_identificado": "Nome do modelo de trança identificado",
          "dificuldade": "Média",
          "tempo_estimado_minutos": 180,
          "observacao": "Uma breve explicação sobre a densidade ou tamanho que influenciou o tempo estimado."
        }
        """

        # Modelos atualizados da SDK google-genai em ordem de prioridade
        modelos_testar = [
            'gemini-2.5-flash',
            'gemini-2.0-flash',
            'gemini-1.5-flash'
        ]

        response = None
        ultimo_erro = None

        for modelo_nome in modelos_testar:
            try:
                response = client.models.generate_content(
                    model=modelo_nome,
                    contents=[prompt, imagem_pil]
                )
                if response and response.text and response.text.strip():
                    break
            except Exception as err:
                ultimo_erro = err
                continue

        if not response or not response.text:
            raise Exception(f"Nenhum modelo respondeu. Último erro: {ultimo_erro}")

        texto_resultado = response.text.strip()

        # Limpa blocos markdown de código
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