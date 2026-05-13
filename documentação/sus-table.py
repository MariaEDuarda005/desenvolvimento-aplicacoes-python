import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Vacinação", layout="wide")

st.title("Vacinação 2025 (API)")

BASE_URL = "https://apidadosabertos.saude.gov.br/vacinacao/doses-aplicadas-pni-2025"


@st.cache_data(ttl=1000)
def load_data(limit, offset):
    params = {
        "limit": limit,
        "offset": offset
    }

    response = requests.get(
        BASE_URL,
        params=params,
        headers={"accept": "application/json"}
    )

    if response.status_code != 200:
        st.error("Erro ao acessar API")
        st.stop()

    data = response.json()

    registros = data.get("doses_aplicadas_pni", [])

    df = pd.json_normalize(registros)
    df.columns = [c.lower() for c in df.columns]

    return df


df = load_data(1000, 1)

st.write(f"Página {100} | Offset {1}")

st.dataframe(df, use_container_width=True)

# =========================
# GRÁFICOS DE ANÁLISE
# =========================

st.subheader("Gráficos de Análise")

col1, col2 = st.columns(2)

# =========================
# RANKING DE VACINAS
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
# MAPA POR ESTADO
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
# LINHA INFERIOR
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
        font_color="black",
        legend_title="Sexo"
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