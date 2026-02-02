import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Medalhas Olímpicas  1967 - 2008",
    page_icon="📊",
    layout="wide",
)

df = pd.read_csv("data/medals_final_modified.csv")

df.columns = df.columns.str.strip().str.lower()

st.sidebar.header("🔍 Filtros")

with st.sidebar.expander("🎯 Filtros principais", expanded=True):

    anos_disponiveis = sorted(df["ano"].dropna().unique())
    anos_selecionados = st.multiselect(
        "Ano", anos_disponiveis, default=anos_disponiveis
    )
    medalhas_disponiveis = sorted(df["medalha"].dropna().unique())
    medalhas_selecionadas = st.multiselect(
        "Medalha", medalhas_disponiveis, default=medalhas_disponiveis
    )

with st.sidebar.expander("⚙️ Filtros avançados", expanded=False):
    esportes_disponiveis = sorted(df["esporte"].dropna().unique())
    esportes_selecionados = st.multiselect(
        "Esporte", esportes_disponiveis, default=esportes_disponiveis
    )

    modalidade_disponiveis = sorted(df["modalidade"].dropna().unique())
    modalidades_selecionadas = st.multiselect(
        "Modalidade", modalidade_disponiveis, default=modalidade_disponiveis
    )

    paises_disponiveis = sorted(df["pais"].dropna().unique())
    paises_selecionados = st.multiselect(
        "País", paises_disponiveis, default=paises_disponiveis
    )

    cidades_disponiveis = sorted(df["cidade"].dropna().unique())
    cidades_selecionadas = st.multiselect(
        "Cidade", cidades_disponiveis, default=cidades_disponiveis
    )

    eventos_disponiveis = sorted(df["event"].dropna().unique())
    eventos_selecionados = st.multiselect(
        "Evento", eventos_disponiveis, default=eventos_disponiveis
    )

    sexos_disponiveis = sorted(df["sexo"].dropna().unique())
    sexos_selecionados = st.multiselect(
        "Sexo", sexos_disponiveis, default=sexos_disponiveis
    )

    atletas_disponiveis = sorted(df["atleta"].dropna().unique())
    atletas_selecionados = st.multiselect(
        "Atleta", atletas_disponiveis, default=atletas_disponiveis
    )


df_filtrado = df[
    (df["ano"].isin(anos_selecionados))
    & (df["esporte"].isin(esportes_selecionados))
    & (df["modalidade"].isin(modalidades_selecionadas))
    & (df["cidade"].isin(cidades_selecionadas))
    & (df["event"].isin(eventos_selecionados))
    & (df["sexo"].isin(sexos_selecionados))
    & (df["pais"].isin(paises_selecionados))
    & (df["medalha"].isin(medalhas_selecionadas))
]

st.title("🎲 Dashboard de Medalhas Olímpicas  1967 - 2008")
st.markdown(
    "Explore os dados de medalhas olímpicas nos últimos anos. Utilize os filtros à esquerda para refinar sua análise."
)

st.subheader("Métricas gerais (Jogos Olímpicos)")

if not df_filtrado.empty:
    total_medalhas = df_filtrado.shape[0]
    total_paises = df_filtrado["pais"].nunique()
    esporte_mais_premiado = df_filtrado["esporte"].mode()[0]
    pais_mais_premiado = df_filtrado["pais"].mode()[0]
    atleta_mais_premiado = df_filtrado["atleta"].mode()[0]
else:
    total_medalhas = 0
    total_paises = 0
    esporte_mais_premiado = "—"
    pais_mais_premiado = "—"
    atleta_mais_premiado = "—"


col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de medalhas", f"{total_medalhas:,}")
col2.metric("Países distintos", f"{total_paises:,}")
col3.metric("Esporte mais premiado", esporte_mais_premiado)
col4.metric("País mais premiado", pais_mais_premiado)
col5.metric("Atleta mais premiado", atleta_mais_premiado)

st.markdown("---")

st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_paises = (
            df_filtrado.groupby("pais")
            .size()
            .nlargest(10)
            .sort_values(ascending=True)
            .reset_index(name="total_medalhas")
        )

        grafico_paises = px.bar(
            top_paises,
            x="total_medalhas",
            y="pais",
            orientation="h",
            title="Top 10 países por número de medalhas",
            labels={"total_medalhas": "Total de medalhas", "pais": ""},
        )

        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_medalhas = px.histogram(
            df_filtrado,
            x="medalha",
            title="Distribuição de medalhas",
            labels={"medalha": "Tipo de medalha", "count": ""},
        )

        grafico_medalhas.update_layout(title_x=0.1)
        st.plotly_chart(grafico_medalhas, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de medalhas.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        sexo_contagem = df_filtrado["sexo"].value_counts().reset_index()
        sexo_contagem.columns = ["sexo", "quantidade"]

        grafico_sexo = px.pie(
            sexo_contagem,
            names="sexo",
            values="quantidade",
            title="Proporção de medalhas por sexo",
            hole=0.5,
        )

        grafico_sexo.update_traces(textinfo="percent+label")
        grafico_sexo.update_layout(title_x=0.1)
        st.plotly_chart(grafico_sexo, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico por sexo.")

with col_graf4:
    if not df_filtrado.empty:
        medalhas_pais = (
            df_filtrado.dropna(subset=["pais_iso3"])
            .groupby("pais_iso3")
            .size()
            .reset_index(name="total_medalhas")
        )

        grafico_mapa = px.choropleth(
            medalhas_pais,
            locations="pais_iso3",
            color="total_medalhas",
            color_continuous_scale="rdylgn",
            title="Total de medalhas por país",
            labels={"total_medalhas": "Total de medalhas", "pais_iso3": "País"},
        )

        grafico_mapa.update_layout(title_x=0.1)
        st.plotly_chart(grafico_mapa, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no mapa de medalhas.")

col_graf5 = st.columns(1)[0]

with col_graf5:
    if not df_filtrado.empty:
        top_atletas = (
            df_filtrado.groupby("atleta")
            .size()
            .nlargest(10)
            .sort_values(ascending=True)
            .reset_index(name="total_medalhas")
        )

        grafico_atletas = px.bar(
            top_atletas,
            x="total_medalhas",
            y="atleta",
            orientation="h",
            title="Top 10 Atletas com mais medalhas",
            labels={"total_medalhas": "Total de medalhas", "atleta": "Atleta"},
            color="total_medalhas",
            color_continuous_scale="Viridis",
        )

        grafico_atletas.update_layout(title_x=0.1, showlegend=False)
        st.plotly_chart(grafico_atletas, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de atletas.")
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)

st.markdown("---")