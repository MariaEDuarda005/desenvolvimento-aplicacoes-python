import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(page_title="Vacinação", layout="wide")

st.title("Vacinação 2025 (JSON Local)")

ARQUIVO = "vacinas_2025.json"


# =========================
# LOAD DATA JSON
# =========================

@st.cache_data(ttl=60)
def load_data():

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        data = json.load(f)

    chave = list(data.keys())[0]

    registros = data.get(chave, [])

    df = pd.json_normalize(registros)

    df.columns = [c.lower() for c in df.columns]

    return df


# =========================
# DADOS
# =========================

df = load_data()

st.write(f"Total de registros: {len(df)}")


# =========================
# TABELA
# =========================

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

colunas_existentes = [
    c for c in colunas_desejadas
    if c in df.columns
]

df_view = df[colunas_existentes]

st.subheader("Tabela")

st.dataframe(
    df_view,
    use_container_width=True,
    height=600
)


# =========================
# GRÁFICOS
# =========================

st.subheader("Gráficos de Análise")

col1, col2 = st.columns(2)

# =========================
# RANKING VACINAS
# =========================
with col1:

    ranking = (
        df["descricao_vacina"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    ranking.columns = ["Vacina", "Quantidade"]

    fig_rank = px.bar(
        ranking.sort_values("Quantidade"),
        x="Quantidade",
        y="Vacina",
        orientation="h",
        text="Quantidade",
        color="Quantidade",
        title="Ranking de Vacinas Aplicadas",
        color_continuous_scale="blues"
    )

    fig_rank.update_layout(
        height=500,
        showlegend=False,
        xaxis_title="Total de doses",
        yaxis_title="",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="black"
    )

    st.plotly_chart(fig_rank, use_container_width=True)

# =========================
# MAPA
# =========================
with col2:

    estados = (
        df["sigla_uf_paciente"]
        .value_counts()
        .reset_index()
    )

    estados.columns = ["UF", "Quantidade"]

    geojson_url = (
        "https://raw.githubusercontent.com/"
        "codeforamerica/click_that_hood/master/"
        "public/data/brazil-states.geojson"
    )

    import requests
    brasil_geojson = requests.get(geojson_url).json()

    fig_mapa = px.choropleth(
        estados,
        geojson=brasil_geojson,
        locations="UF",
        featureidkey="properties.sigla",
        color="Quantidade",
        hover_name="UF",
        color_continuous_scale="blues",
        title="Distribuição Geográfica"
    )

    fig_mapa.update_geos(
        fitbounds="locations",
        visible=False
    )

    fig_mapa.update_layout(
        height=500,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="black"
    )

    st.plotly_chart(fig_mapa, use_container_width=True)

# =========================
# LINHA DE BAIXO
# =========================

col3, col4, col5 = st.columns(3)

# =========================
# SEXO
# =========================
with col3:

    sexo = (
        df["tipo_sexo_paciente"]
        .value_counts()
        .reset_index()
    )

    sexo.columns = ["Sexo", "Quantidade"]

    sexo["Sexo"] = sexo["Sexo"].replace({
        "M": "Masculino",
        "F": "Feminino"
    })

    fig_sexo = px.pie(
        sexo,
        names="Sexo",
        values="Quantidade",
        hole=0.5,
        title="Sexo",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    fig_sexo.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="black"
    )

    st.plotly_chart(fig_sexo, use_container_width=True)

# =========================
# FAIXA ETÁRIA
# =========================
with col4:

    idade = df.copy()

    idade["numero_idade_paciente"] = pd.to_numeric(
        idade["numero_idade_paciente"],
        errors="coerce"
    )

    bins = [0, 4, 11, 17, 29, 39, 49, 59, 120]

    labels = [
        "0 a 4",
        "5 a 11",
        "12 a 17",
        "18 a 29",
        "30 a 39",
        "40 a 49",
        "50 a 59",
        "60+"
    ]

    idade["faixa_etaria"] = pd.cut(
        idade["numero_idade_paciente"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    faixa = (
        idade["faixa_etaria"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    faixa.columns = ["Faixa Etária", "Quantidade"]

    fig_faixa = px.bar(
        faixa,
        x="Faixa Etária",
        y="Quantidade",
        text="Quantidade",
        color="Quantidade",
        title="Faixa Etária",
        color_continuous_scale="blues"
    )

    fig_faixa.update_layout(
        height=400,
        showlegend=False,
        xaxis_title="Faixa etária",
        yaxis_title="Total de doses",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="black"
    )

    st.plotly_chart(fig_faixa, use_container_width=True)

# =========================
# COR / RAÇA
# =========================
with col5:

    raca = (
        df["nome_raca_cor_paciente"]
        .value_counts()
        .reset_index()
    )

    raca.columns = ["Raça", "Quantidade"]

    fig_raca = px.pie(
        raca,
        names="Raça",
        values="Quantidade",
        hole=0.5,
        title="Cor/Raça",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    fig_raca.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="black"
    )

    st.plotly_chart(fig_raca, use_container_width=True)