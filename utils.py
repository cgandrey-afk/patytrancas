import streamlit as st
import google.generativeai as genai
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
        
        # 2. Garante que o ponteiro do arquivo enviado esteja no início (resolve leitura de 0 bytes)
        imagem_upload.seek(0)
        bytes_imagem = imagem_upload.read()
        imagem_pil = Image.open(io.BytesIO(bytes_imagem))
        
        prompt = """
        Você é um especialista em penteados e tranças afro.
        Analise a imagem enviada e estime a complexidade e o tempo necessário para executar o penteado.
        
        Retorne ESTRITAMENTE um JSON com esta estrutura exata (sem formatação markdown como ```json):
        {
          "estilo_identificado": "Nome do modelo de trança identificado",
          "dificuldade": "Média",
          "tempo_estimado_minutos": 180,
          "observacao": "Uma breve explicação sobre a densidade ou tamanho que influenciou o tempo estimado."
        }
        """

        # 3. Modelos suportados organizados por prioridade
        modelos_tentativa = [
            'gemini-1.5-flash',
            'models/gemini-1.5-flash',
            'gemini-1.5-pro',
            'models/gemini-1.5-pro'
        ]

        # Configuração para requerer JSON nativo
        generation_config = {
            "response_mime_type": "application/json"
        }

        response = None
        ultimo_erro = None

        for nome_modelo in modelos_tentativa:
            try:
                model = genai.GenerativeModel(
                    model_name=nome_modelo,
                    generation_config=generation_config
                )
                response = model.generate_content([prompt, imagem_pil])
                
                # Se obtivemos uma resposta válida com candidato
                if response and response.candidates and len(response.candidates) > 0:
                    cand = response.candidates[0]
                    # Verifica se o motivo de finalização foi STOP (sucesso)
                    if cand.content and cand.content.parts:
                        break
            except Exception as err:
                ultimo_erro = err
                continue

        # 4. Extração e validação do texto retornado
        if not response or not response.text or not response.text.strip():
            raise Exception("A IA não gerou conteúdo para esta imagem. Tente enviar outra foto com melhor iluminação.")

        texto_limpo = response.text.strip()
        
        # Remove eventuais blocos de código markdown se houver
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