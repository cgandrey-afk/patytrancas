import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Paty Tranças - Agendamento & Catálogo",
    page_icon="👑",
    layout="wide"
)

# Sidebar - Menu de Navegação
st.sidebar.title("👑 Paty Tranças")
st.sidebar.markdown("---")

opcao_menu = st.sidebar.radio(
    "Navegação:",
    [
        "📖 Catálogo",
        "🗓️ Agendar",
        "📸 Trança com IA",
        "🖼️ Meus Trabalhos",
        "🔒 Área Administrativa"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido para otimizar seus atendimentos.")

# Roteamento das Páginas
if opcao_menu == "📖 Catálogo":
    st.title("📖 Catálogo de Estilos & Preços")
    st.write("Conheça nossos modelos de tranças, valores base e tempo estimado de execução.")
    # Aqui vai o código que exibe os cards dos modelos cadastrados

elif opcao_menu == "🗓️ Agendar":
    st.title("🗓️ Faça seu Agendamento")
    st.write("Escolha o modelo desejado, selecione o melhor dia e horário para seu atendimento.")
    # Aqui vai o formulário de agendamento

elif opcao_menu == "📸 Trança com IA":
    st.title("📸 Análise de Penteado com IA")
    st.write("Envie uma foto da trança desejada para estimarmos o tempo exato com base na complexidade e no seu cabelo.")
    # Aqui chamamos a função 'analisar_imagem_com_gemini' do utils.py

elif opcao_menu == "🖼️ Meus Trabalhos":
    st.title("🖼️ Galeria de Trabalhos Realizados")
    st.write("Confira os resultados reais dos penteados e tranças feitos em nossas clientes!")
    # Aqui vai a galeria estilo mural/grid de fotos reais

elif opcao_menu == "🔒 Área Administrativa":
    st.title("🔒 Painel da Trancista")
    # Aqui vai a validação de senha e o gerenciamento do sistema