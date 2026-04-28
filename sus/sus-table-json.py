import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Vacinação", layout="wide")

st.title("Vacinação 2025 (JSON Local)")

st.sidebar.header("Paginação para a tabela")

limit = st.sidebar.selectbox("Linhas por página", [10, 25, 50, 100], index=1)
page = st.sidebar.number_input("Página", min_value=1, step=1)

offset = (page - 1) * limit

ARQUIVO = "vacinas_2025.json"


@st.cache_data(ttl=60)
def load_data(limit, offset):

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        data = json.load(f)

    chave = list(data.keys())[0]
    registros = data.get(chave, [])

    total = len(registros)

    # paginação
    registros_pagina = registros[offset:offset+limit]

    df = pd.json_normalize(registros)
    df.columns = [c.lower() for c in df.columns]

    df_pagina = pd.json_normalize(registros_pagina)
    df_pagina.columns = [c.lower() for c in df_pagina.columns]

    return df, df_pagina, total

df_base, df_page, total = load_data(limit, offset)

st.write(f"Página {page}")
st.write(f"Mostrando {len(df_page)} de {total} registros")

colunas_desejadas = [
    "descricao_natureza_estabelecimento",
    "nome_pais_paciente",
    "nome_raca_cor_paciente",
    "data_vacina",
    "nome_razao_social_estabelecimento",
    "sigla_uf_estabelecimento",
    "nome_municipio_estabelecimento",
    "descricao_tipo_estabelecimento",
    "descricao_estrategia_vacinacao",
    "nome_uf_paciente",
    "sigla_uf_paciente",
    "nome_uf_estabelecimento",
    "descricao_vacina",
    "tipo_sexo_paciente"
]

colunas_existentes = [c for c in colunas_desejadas if c in df_page.columns]

df_view = df_page[colunas_existentes]

st.subheader("Tabela")
st.dataframe(df_view, use_container_width=True)

st.subheader("Doses por sexo (dados completos)")

if "tipo_sexo_paciente" in df_base.columns:
    grafico = df_base["tipo_sexo_paciente"].value_counts().reset_index()
    grafico.columns = ["sexo", "quantidade"]

    st.bar_chart(grafico.set_index("sexo"))
else:
    st.warning("Coluna 'tipo_sexo_paciente' não encontrada")