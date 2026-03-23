import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import time

st.set_page_config(page_title="Criptomoedas", layout="wide")

st.title("📊 Dashboard de Criptomoedas")

# 🔄 Atualização automática
atualizar = st.sidebar.checkbox("Atualizar automaticamente")
intervalo = st.sidebar.slider("Intervalo (segundos)", 10, 60, 30)

# 🔎 Filtro de quantidade
quantidade = st.sidebar.slider("Quantidade de moedas", 5, 50, 10)

url = "https://api.coingecko.com/api/v3/coins/markets"

def carregar_dados(qtd):
    parametros = {
        "vs_currency": "brl",
        "order": "market_cap_desc",
        "per_page": qtd,
        "page": 1
    }
    resposta = requests.get(url, params=parametros)
    return resposta.json()

dados = carregar_dados(quantidade)

# 📦 DataFrame
df = pd.DataFrame(dados)[[
    "name",
    "current_price",
    "price_change_percentage_24h",
    "market_cap_rank"
]]

df.columns = ["Criptomoeda", "Preço (R$)", "Variação 24h (%)", "Ranking"]

# 📋 Tabela
st.subheader("📋 Dados")
st.dataframe(df, use_container_width=True)

# 📊 Gráfico de preço
st.subheader("💰 Preço das criptomoedas")
fig1 = px.bar(
    df,
    x="Preço (R$)",
    y="Criptomoeda",
    orientation="h",
    color="Preço (R$)",
    color_continuous_scale="blues"
)
st.plotly_chart(fig1, use_container_width=True)

# 📉 Gráfico de variação
st.subheader("📉 Variação nas últimas 24h")
fig2 = px.bar(
    df,
    x="Variação 24h (%)",
    y="Criptomoeda",
    orientation="h",
    color="Variação 24h (%)",
    color_continuous_scale="RdYlGn"
)
st.plotly_chart(fig2, use_container_width=True)

# 🔄 Auto refresh
if atualizar:
    time.sleep(intervalo)
    st.rerun()