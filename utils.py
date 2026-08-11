import os
import json
import io
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

def carregar_css():
    """Carrega o arquivo CSS externo e injeta na aplicação de forma segura."""
    caminho_css = "style.css"
    if os.path.exists(caminho_css):
        try:
            with open(caminho_css, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Erro ao ler o arquivo style.css: {e}")
    else:
        st.warning("⚠️ O arquivo 'style.css' não foi encontrado na raiz do projeto. Verifique o repositório no GitHub.")


def formatar_tempo(minutos):
    """Formata minutos no formato legível de horas e minutos."""
    try:
        minutos = int(minutos)
    except (ValueError, TypeError):
        return "Tempo a definir"
        
    horas = minutos // 60
    min_restantes = minutos % 60
    if horas > 0 and min_restantes > 0:
        return f"{horas}h {min_restantes}min"
    elif horas > 0:
        return f"{horas}h"
    return f"{min_restantes}min"


def analisar_imagem_com_gemini(imagem_upload):
    """Envia a imagem para a API Gemini e retorna a estimativa de tempo e complexidade em JSON."""
    try:
        # 1. Chave e Cliente da SDK oficial
        api_key = st.secrets["gemini"]["api_key"]
        client = genai.Client(api_key=api_key)
        
        # 2. Processa a imagem para garantir compatibilidade RGB
        imagem_upload.seek(0)
        bytes_imagem = imagem_upload.read()
        imagem_pil = Image.open(io.BytesIO(bytes_imagem))
        
        if imagem_pil.mode in ("RGBA", "P"):
            imagem_pil = imagem_pil.convert("RGB")
        
        prompt = """
        Você é uma trancista profissional e especialista em penteados afro e nagô.
        Analise a imagem enviada e estime a complexidade e o TEMPO REAL com base na tabela e nas regras abaixo:

        TABELA DE REFERÊNCIA DE TEMPO E COMPLEXIDADE:

        1. DESENHO E COMPLEXIDADE DO TOPO/LATERAL:
           - TRANÇAS SIMPLES OU RETAS (Laterais ou Tiara):
             * Cabelo Liso/Ondulado: 60 a 90 minutos (1h a 1h30min).
             * Cabelo Cacheado/Crespo: 90 a 120 minutos (1h30min a 2h).

           - DESENHOS DE ALTA PRECISÃO, GEOMÉTRICOS OU SIMÉTRICOS (Ex: Formato de Coração, Cruzados/X, Borboleta, Tiara trabalhada com curvas e acessórios no topo):
             * Exige divisão minuciosa e alinhamento preciso dos fios.
             * Cabelo Liso/Ondulado: 120 a 150 minutos (2h a 2h30min).
             * Cabelo Cacheado/Crespo/Afro: 150 a 180 minutos (2h30min a 3h).

        2. PENTEADOS COMPLETOS / CABEÇA TODA:
           - Meia cabeça (Nagô até a metade): 2h a 3h.
           - Cabeça toda (Nagô completa / Fulani / Box Braids): 3h a 6h+.

        3. AVALIAÇÃO VISUAL OBRIGATÓRIA DA IMAGEM:
           - Observe a curvatura do cabelo nas raízes e pontas (Liso vs. Cacheado/Crespo).
           - Identifique se há desenhos elaborados (corações, cruzamentos, formas geométricas) que exigem simetria rigorosa.

        Retorne ESTRITAMENTE um objeto JSON no seguinte formato:
        {
          "estilo_identificado": "Nagô Topo com Desenho Geométrico/Coração e Acessórios",
          "dificuldade": "Alta",
          "tempo_estimado_minutos": 180,
          "observacao": "Explicação detalhada destacando a complexidade do desenho simétrico/cruzado no topo e a textura do cabelo."
        }
        """

        # Modelos recomendados em ordem de preferência
        modelos_fallback = [
            'gemini-2.5-flash',
            'gemini-2.0-flash'
        ]

        response = None
        ultimo_erro = None

        # Configuração para forçar resposta em JSON puro
        config_geracao = types.GenerateContentConfig(
            response_mime_type="application/json"
        )

        for modelo_nome in modelos_fallback:
            try:
                response = client.models.generate_content(
                    model=modelo_nome,
                    contents=[prompt, imagem_pil],
                    config=config_geracao
                )
                if response and response.text and response.text.strip():
                    break
            except Exception as err:
                ultimo_erro = err
                continue

        if not response or not response.text:
            raise Exception(f"Nenhum modelo disponível respondeu. Detalhe: {ultimo_erro}")

        texto_resultado = response.text.strip()

        # Limpeza preventiva caso haja blocos de código Markdown
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