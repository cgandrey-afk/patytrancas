import streamlit as st
from utils import analisar_imagem_com_gemini, formatar_tempo

def render():
    st.title("📸 Trança Personalizada")
    st.write("Envie uma foto da trança desejada. Nossa IA analisará o modelo para estimar a complexidade e o tempo necessário!")

    foto = st.file_uploader("Selecione ou tire uma foto", type=["jpg", "jpeg", "png"])

    if foto:
        st.image(foto, caption="Foto enviada", use_container_width=True)
        
        if st.button("Analisar Trança com IA"):
            with st.spinner("Analisando detalhes do modelo..."):
                resultado = analisar_imagem_com_gemini(foto)
                
                if resultado:
                    st.success("Análise Concluída!")
                    st.markdown(f"**Estilo Identificado:** {resultado.get('estilo_identificado', 'Personalizado')}")
                    st.markdown(f"**Dificuldade:** {resultado.get('dificuldade', 'Não informada')}")
                    
                    tempo_min = resultado.get('tempo_estimado_minutos', 180)
                    st.markdown(f"**Tempo Estimado:** {formatar_tempo(tempo_min)}")
                    st.info(f"💡 {resultado.get('observacao', '')}")
                    
                    if st.button("Buscar Horários para este Modelo"):
                        st.session_state['tranca_selecionada'] = {
                            "nome": resultado.get('estilo_identificado', 'Modelo Personalizado'),
                            "tempo_min": tempo_min,
                            "preco": "A combinar"
                        }
                        st.success("Modelo selecionado! Navegue até a aba 'Catálogo / Agendar' para escolher o horário.")