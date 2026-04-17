import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="BKS Distribuidora", page_icon="💊")

# Estilização básica
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# 1. Saudação e Nome da Empresa
st.title("🇧🇷 BKS DISTRIBUIDORA DE MEDICAMENTOS")

# Inicializar estados de controle
if 'consulta_ativa' not in st.session_state:
    st.session_state.consulta_ativa = True

def encerrar():
    st.session_state.consulta_ativa = False

def reiniciar_consulta():
    # Limpa as chaves de busca para permitir nova entrada
    if "busca" in st.session_state:
        st.session_state.busca = ""
    st.rerun()

if st.session_state.consulta_ativa:
    # 2. Qual o seu nome
    nome_usuario = st.text_input("Olá! Bem-vindo ao sistema. Qual é o seu nome?", key="nome")

    if nome_usuario:
        st.write(f"Muito prazer, **{nome_usuario}**! Vamos iniciar sua consulta.")

        # 3. Carregamento do arquivo
        url = "https://docs.google.com/spreadsheets/d/1ltaHWxs36rhlT27kMuM6BWNOyTjLCH1Q/export?format=xlsx"
        
        @st.cache_data
        def carregar_dados(url_planilha):
            return pd.read_excel(url_planilha, header=1)

        try:
            df = carregar_dados(url)
            
            # 4. Qual o Cód. Referência você deseja
            cod_busca = st.text_input("Digite o Cód. Referência que deseja consultar:", key="busca")

            if cod_busca:
                # 5. Procure o código de referência
                filtro = df[df['Cód. Referência'].astype(str) == str(cod_busca)]

                if filtro.empty:
                    # 6 e 7. Caso não ache, informa e permite nova tentativa
                    st.error("⚠️ Código não cadastrado!!! Por favor, verifique o número e tente novamente.")
                else:
                    # 8. Soma a Qtd. Disponível
                    soma_qtd = filtro['Qtd. Disponível'].sum()
                    
                    # 9. Informe o Cód. Referência e a soma
                    st.success(f"### Resultado para o Código: {cod_busca}")
                    st.metric(label="Total Disponível em Estoque", value=int(soma_qtd))
                    
                    # REATIVADO: Mostrar a lista de itens encontrados
                    with st.expander("Clique aqui para ver a lista detalhada de lotes"):
                        st.dataframe(filtro[['Cód. Referência', 'Descrição', 'Nº Lote', 'Dt. Produção', 'Qtd. Disponível', 'Observação']])
                    
                    st.divider()
                    
                    # 10 e 11. Pergunta se deseja consultar outro código
                    st.write("### Deseja consultar outro código?")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # O botão "Sim" agora chama a função de limpeza e reinício
                        if st.button("✅ SIM (Nova consulta)"):
                            reiniciar_consulta()
                            
                    with col2:
                        if st.button("❌ NÃO (Encerrar)"):
                            encerrar()
                            st.rerun()

        except Exception as e:
            st.error(f"Erro ao acessar a base de dados: {e}")
else:
    # Tela de encerramento
    st.balloons()
    st.success("Consulta finalizada!")
    st.write("Obrigado por utilizar o sistema da **BKS Distribuidora de Medicamentos**.")
    if st.button("Fazer nova consulta"):
        st.session_state.consulta_ativa = True
        st.rerun()

st.divider()
st.caption("BKS Distribuidora - Sistema de Gestão de Estoque")
