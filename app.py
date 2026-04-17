import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="BKS Distribuidora", page_icon="💊")

# 1. Saudação e Nome da Empresa
st.title("🇧🇷 BKS DISTRIBUIDORA DE MEDICAMENTOS")
st.subheader("Sistema de Consulta de Estoque")

# 2. Identificação do Usuário
nome_usuario = st.text_input("Qual é o seu nome?")

if nome_usuario:
    st.write(f"Olá, **{nome_usuario}**! Vamos realizar a sua consulta.")

    # 3. Carregamento do arquivo
    url = "https://docs.google.com/spreadsheets/d/1ltaHWxs36rhlT27kMuM6BWNOyTjLCH1Q/export?format=xlsx"
    
    @st.cache_data
    def carregar_dados(url_planilha):
        return pd.read_excel(url_planilha, header=1)

    try:
        df = carregar_dados(url)
        
        # 4. Entrada do Código de Referência
        cod_busca = st.text_input("Digite o Cód. Referência que deseja consultar:")

        if cod_busca:
            # 5. Procura o código
            filtro = df[df['Cód. Referência'].astype(str) == str(cod_busca)]

            if not filtro.empty:
                # 8. Soma a Qtd. Disponível
                soma_qtd = filtro['Qtd. Disponível'].sum()
                
                # 9. Exibe o Resultado
                st.success(f"### Resultado para o Código: {cod_busca}")
                st.metric(label="Total Disponível em Estoque", value=int(soma_qtd))
                
                # Exibir detalhes se necessário
                with st.expander("Ver detalhes dos lotes"):
                    st.dataframe(filtro[['Nº Lote', 'Dt. Produção', 'Qtd. Disponível', 'Observação']])
            else:
                # 6. Caso não ache
                st.error("⚠️ Código não cadastrado!!!")
                
    except Exception as e:
        st.error(f"Erro ao conectar com a base de dados: {e}")

st.divider()
st.caption("BKS Distribuidora - Todos os direitos reservados.")