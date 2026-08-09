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

        Retorne ESTRITAMENTE um objeto JSON no seguinte formato (sem marcações markdown adicionais):
        {
          "estilo_identificado": "Nagô Topo com Desenho Geométrico/Coração e Acessórios",
          "dificuldade": "Alta",
          "tempo_estimado_minutos": 180,
          "observacao": "Explicação detalhada destacando a complexidade do desenho simétrico/cruzado no topo e a textura do cabelo."
        }
        """

        # 3. Descobre dinamicamente os modelos ativos na sua chave de API
        modelos_disponiveis = []
        try:
            for m in client.models.list():
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

        # Limpa blocos de formatação markdown
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

def render():
    """Renderiza a interface da Análise com IA no Streamlit."""
    with st.container(border=True):
        st.markdown('<h3 style="color: #e05297; margin-bottom: 5px;">✨ Estimativa Inteligente de Penteado</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666; font-size: 0.9rem;">Envie uma foto do estilo de trança desejado para nossa IA analisar a complexidade e o tempo estimado de atendimento.</p>', unsafe_allow_html=True)
        st.divider()

        upload_foto = st.file_uploader(
            "Envie a imagem do penteado (JPG, JPEG ou PNG):", 
            type=["jpg", "jpeg", "png"]
        )

        if upload_foto is not None:
            col1, col2 = st.columns([1, 1])

            with col1:
                st.image(upload_foto, caption="Foto enviada", use_container_width=True)

            with col2:
                btn_analisar = st.button("🔍 Analisar Penteado com IA", use_container_width=True)

                if btn_analisar:
                    with st.spinner("Analisando complexidade e estimando o tempo..."):
                        resultado = analisar_imagem_com_gemini(upload_foto)

                    if resultado:
                        st.success("Análise concluída!")
                        
                        st.markdown(f"**Estilo Identificado:** {resultado.get('estilo_identificado', 'N/A')}")
                        st.markdown(f"**Dificuldade:** `{resultado.get('dificuldade', 'N/A')}`")
                        
                        tempo_min = resultado.get('tempo_estimado_minutos', 0)
                        tempo_formatado = formatar_tempo(tempo_min)
                        st.markdown(f"⏱️ **Tempo Estimado:** `{tempo_formatado}`")
                        
                        st.info(f"💡 **Observação da IA:**\n{resultado.get('observacao', '')}")