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
        Analise a imagem enviada para estimar a complexidade e o TEMPO REAL de execução do trabalho.

        REGRAS RÍGIDAS DE ESTIMATIVA DE TEMPO (MÁXIMOS E MÍNIMOS):

        1. COBERTURA DA CABEÇA (CRITÉRIO PRINCIPAL):
           - TRANÇA PARCIAL / LATERAL / TIARA (Como na foto, cobrindo apenas uma lateral ou topo do cabelo, deixando o restante solto):
             -> Cabelo Liso/Ondulado: Duração MÁXIMA de 60 a 90 minutos (1h a 1h30min).
             -> Cabelo Crespo/Afro: Duração de 90 a 120 minutos (1h30min a 2h).
           - MEIA CABEÇA (Nagô até a metade):
             -> 1h30min a 2h30min.
           - CABEÇA TODA (Nagô completa, Fulani Braids completas ou Box Braids):
             -> 3h a 6h+.

        2. INFLUÊNCIA DA TEXTURA DO CABELO:
           - Cabelo liso/ondulado visualizado: Reduza a estimativa. O manuseio e a divisão são mais rápidos.
           - Cabelo crespo/afro volumoso: Exige mais alinhamento e pomada, mantendo o tempo padrão.

        3. DETALHES (DESENHOS E ACESSÓRIOS):
           - Curvas, fitas e anéis em tranças PARCIAIS aumentam a complexidade, mas NÃO devem fazer o tempo total ultrapassar 90 a 105 minutos se for apenas uma lateral.

        Retorne ESTRITAMENTE um objeto JSON no seguinte formato (sem formatação markdown adicionais):
        {
          "estilo_identificado": "Nagô Lateral Ondulada com Acessórios",
          "dificuldade": "Média",
          "tempo_estimado_minutos": 90,
          "observacao": "Explicação objetiva justificando o tempo com base no fato de ser apenas uma lateral/penteado parcial em cabelo liso."
        }
        """

        # 3. Descobre dinamicamente os modelos ativos na sua chave de API
        modelos_disponiveis = []
        try:
            for m in client.models.list():
                # Filtra apenas modelos que suportam generateContent
                if hasattr(m, 'supported_actions') and 'generateContent' in m.supported_actions:
                    nome_limpo = m.name.replace("models/", "")
                    modelos_disponiveis.append(nome_limpo)
        except Exception:
            pass

        # Lista de fallback caso a listagem dinâmica falhe
        if not modelos_disponiveis:
            modelos_disponiveis = [
                'gemini-2.5-flash',
                'gemini-2.0-flash'
            ]

        response = None
        ultimo_erro = None

        for modelo_nome in modelos_disponiveis:
            # Pula modelos experimentais ou de embeddings se existirem na lista
            if "embedding" in modelo_nome or "imagen" in modelo_nome:
                continue
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
            raise Exception(f"Nenhum modelo disponível respondeu. Detalhe: {ultimo_erro}")

        texto_resultado = response.text.strip()

        # Limpa blocos de formatação markdown caso a IA inclua ```json ... ```
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