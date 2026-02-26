import streamlit as st
import pandas as pd
import plotly.express as px

DEPARTEMENTS_OCCITANIE = [
    "09","11","12","30","31","32","34",
    "46","48","65","66","81","82"
]

DEPARTEMENTS_NOMS = {
    "31": "Haute-Garonne",
    "34": "Hérault",
    "30": "Gard",
    "11": "Aude",
    "12": "Aveyron",
    "09": "Ariège",
    "32": "Gers",
    "48": "Lozère",
    "65": "Hautes-Pyrénées",
    "66": "Pyrénées-Orientales",
    "46": "Lot",
    "81": "Tarn",
    "82": "Tarn-et-Garonne"
}

# ========================
# PALETTE COULEURS
# ========================

BLEU_NUIT = "#1F2A44"
PRUNE = "#6C3B8E"
TERRACOTTA = "#C05A2B"
SABLE = "#D8A47F"
FRAMBOISE = "#A13D63"

def style_fig(fig):
    fig.update_layout(
        template="simple_white",
        font=dict(family="Inter, sans-serif", size=14),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            orientation="v",
            y=1,
            yanchor="top",
            x=1.02,
            xanchor="left"
        )
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=6))
    return fig

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/toutes_causes.csv")

@st.cache_data
def load_detail():
    return pd.read_csv("data/processed/mortalite_standardise_2010-2023.csv")

# ========================
# AXE 2 — DYNAMIQUE
# ========================

def render_dynamique():

    # ----------------------
    # TITRE + INTRO
    # ----------------------
    st.title("📈 Dynamique temporelle 2010–2023")

    st.markdown("""
    Cet axe permet d’identifier les tendances de long terme, 
    les ruptures conjoncturelles et les écarts structurels.
    """)

    st.divider()

    # ----------------------
    # DONNÉES
    # ----------------------
    df = load_data()
    df_detail = load_detail()

    df_global = df[
        (df["cause"] == "Toutes causes") &
        (df["sexe"] == "Tous sexes")
    ]

    # ----------------------
    # 1️⃣ ÉVOLUTION GLOBALE
    # ----------------------
    st.header("1️⃣ Évolution globale Occitanie / France")

    # Occitanie
    df_occ = (
        df_global[df_global["departement"].isin(DEPARTEMENTS_OCCITANIE)]
        .groupby("annee")["valeur"]
        .mean()
        .reset_index()
    )
    df_occ["territoire"] = "Occitanie"

    # France
    df_fr = (
        df_global
        .groupby("annee")["valeur"]
        .mean()
        .reset_index()
    )
    df_fr["territoire"] = "France"

    df_plot = pd.concat([df_occ, df_fr])

    fig = px.line(
        df_plot,
        x="annee",
        y="valeur",
        color="territoire",
        template="simple_white",
        color_discrete_sequence=[PRUNE, BLEU_NUIT],
        labels={
            "valeur": "Taux standardisé (pour 100 000)",
            "annee": "Année"
        }
    )

    fig.add_annotation(
    x=2020,
    y=df_plot["valeur"].max(),
    text="Choc COVID",
    showarrow=True,
    arrowhead=2
    )

    fig = style_fig(fig)

    st.plotly_chart(fig, use_container_width=True)

    st.info(
    "La mortalité diminue progressivement jusqu’en 2019, "
    "avec une rupture nette en 2020 liée au choc sanitaire. "
    "L’Occitanie évolue parallèlement à la France, sans divergence structurelle."
    )

    st.divider()

    # ----------------------
    #  2️⃣ Évolution par grandes causes en Occitanie
    # ----------------------
    st.header("2️⃣ Évolution par grandes causes en Occitanie")

    # Filtrer Occitanie + Tous sexes
    df_detail_occ = df_detail[
        (df_detail["sexe"] == "Tous sexes") &
        (df_detail["departement"].isin(DEPARTEMENTS_OCCITANIE))
    ]

    # 3 grandes causes seulement
    causes_interessantes = [
        "7. Maladies de l’appareil circulatoire",
        "2. Tumeurs",
        "8. Maladies de l’appareil respiratoire"
    ]

    df_causes = df_detail_occ[df_detail_occ["cause"].isin(causes_interessantes)]

    # Moyenne régionale
    df_causes = (
        df_causes
        .groupby(["annee", "cause"])["valeur"]
        .mean()
        .reset_index()
    )

    fig_causes = px.line(
        df_causes,
        x="annee",
        y="valeur",
        color="cause",
        template="simple_white",
    color_discrete_sequence=[FRAMBOISE, TERRACOTTA, SABLE],
    labels={
        "valeur": "Taux standardisé (pour 100 000)",
        "annee": "Année",
        "cause": "Cause"
    }
)

    fig_causes = style_fig(fig_causes)

    fig_causes.update_layout(
    legend=dict(
        orientation="v",
        y=1,
        yanchor="top",
        x=1.02,
        xanchor="left"
    )
)

    st.plotly_chart(fig_causes, use_container_width=True)

    st.info(
    "Les maladies cardiovasculaires diminuent structurellement. "
    "Les pathologies respiratoires présentent une rupture en 2020–2021. "
    "Les tendances restent parallèles aux dynamiques nationales."
    )

    st.divider()

    # ----------------------
    # 3️⃣ Évolution par sexe et par cause en Occitanie
    # ----------------------
    st.header("3️⃣ Différences hommes / femmes par grande cause en Occitanie")

    # Filtrer Occitanie uniquement
    df_sexe = df_detail[
        (df_detail["departement"].isin(DEPARTEMENTS_OCCITANIE)) &
        (df_detail["sexe"].isin(["Hommes", "Femmes"])) &
        (df_detail["cause"].isin([
            "7. Maladies de l’appareil circulatoire",
            "2. Tumeurs",
            "8. Maladies de l’appareil respiratoire"
        ]))
    ]

    # Moyenne régionale
    df_sexe = (
        df_sexe
        .groupby(["annee", "sexe", "cause"])["valeur"]
        .mean()
        .reset_index()
    )

    fig_sexe = px.line(
        df_sexe,
        x="annee",
        y="valeur",
        color="sexe",
        facet_col="cause",
        height=450,
        template="simple_white",
        color_discrete_sequence=[PRUNE, TERRACOTTA],
        labels={
            "valeur": "Taux standardisé (pour 100 000)",
            "annee": "Année",
            "sexe": "Sexe",
            "cause": ""
        }
    )

    fig_sexe.update_traces(line=dict(width=3))
    fig_sexe.update_layout(
        height=450,
        font=dict(family="Inter, sans-serif", size=13),
        margin=dict(l=20, r=40, t=40, b=20),
        legend=dict(
            orientation="v",
            y=1,
            yanchor="top",
            x=1.02,
            xanchor="left"
        )
    )

    fig_sexe.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    st.plotly_chart(fig_sexe, use_container_width=True)

    st.info(
    "Les hommes présentent des niveaux de mortalité supérieurs aux femmes, "
    "avec un écart particulièrement marqué pour les maladies cardiovasculaires. "
    "Ces écarts traduisent des dynamiques de genre complexes en matière de santé."
    )

    st.divider()
     