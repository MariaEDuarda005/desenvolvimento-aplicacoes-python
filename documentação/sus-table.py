import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Vacinação", layout="wide")

st.title("Vacinação 2025 (API)")

BASE_URL = "https://apidadosabertos.saude.gov.br/vacinacao/doses-aplicadas-pni-2025"

# st.sidebar.header("Paginação")

# limit = st.sidebar.selectbox("Linhas por página", [10, 25, 50, 100], index=1)
# page = st.sidebar.number_input("Página", min_value=1, step=1)

# offset = (page - 1) * limit

@st.cache_data(ttl=60)
def load_data(limit, offset):
    params = {
        "limit": limit,
        "offset": offset
    }

    response = requests.get(BASE_URL, params=params, headers={"accept": "application/json"})
    
    if response.status_code != 200:
        st.error("Erro ao acessar API")
        st.stop()

    data = response.json()
    
    registros = data.get("doses_aplicadas_pni", [])
    
    df = pd.json_normalize(registros)
    df.columns = [c.lower() for c in df.columns]

    return df

df = load_data(60, 1)

st.write(f"Página {60} | Offset {1}")

st.dataframe(df, use_container_width=True)