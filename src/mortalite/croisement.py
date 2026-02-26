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

@st.cache_data
def load_urbanite():
    return pd.read_csv("data/processed/urbanite.csv")

@st.cache_data
def load_mortalite():
    df = pd.read_csv("data/processed/mortalite_2023_standardise_all.csv")

    df = (
        df[df["annee"] == 2023]
        .query("sexe == 'Tous sexes'")
        .groupby("departement", as_index=False)["valeur"]
        .sum()
        .rename(columns={"valeur": "taux_total"})
    )
    return df

def render_croisement():
    st.title("⚖️ Déterminants territoriaux et mortalité")

    st.markdown(
    "Lien entre accessibilité aux soins et mortalité départementale (2023)."
    )

    df_mort = load_mortalite()
    df_urbanite = load_urbanite()

    # Important : harmoniser types
    df_mort["departement"] = df_mort["departement"].astype(str)
    df_urbanite["code_dept"] = df_urbanite["code_dept"].astype(str)

    df_merge = df_mort.merge(
    df_urbanite,
    left_on="departement",
    right_on="code_dept",
    how="inner"
)

    st.divider()

    # ----------------------
    # 1️⃣ Corrélation nationale
    # ----------------------
    st.header("1️⃣ Densité médicale par département de France métropolitaine")

    fig_nat = px.scatter(
    df_merge,
    x="apl_medecins_std",
    y="taux_total",
    trendline="ols",
    color_discrete_sequence=[PRUNE]
    )

    fig_nat.update_layout(
        xaxis_title="Densité médicale (score standardisé)",
        yaxis_title="Taux standardisé de mortalité (2023)"
    )

    st.plotly_chart(fig_nat, use_container_width=True)

    st.info(
    "Au niveau national, la relation entre densité médicale et mortalité apparaît modérée. "
    )

    st.divider()

    # ----------------------
    # 2️⃣ Zoom Occitanie
    # ----------------------
    st.header("2️⃣ Densité médicale par département en Occitanie")

    df_occ = df_merge[df_merge["departement"].isin(DEPARTEMENTS_OCCITANIE)]

    fig_occ = px.scatter(
        df_occ,
        x="apl_medecins_std",
        y="taux_total",
        trendline="ols",
        color_discrete_sequence=[TERRACOTTA]
    )

    fig_occ.update_layout(
        xaxis_title="Densité médicale (score standardisé)",
        yaxis_title="Taux standardisé de mortalité (2023)"
    )

    st.plotly_chart(fig_occ, use_container_width=True)

    st.info(
    "En Occitanie, la dynamique est comparable, suggérant que l’offre de soins constitue un facteur parmi d’autres "
    "dans l’explication des écarts territoriaux."
    )

    st.divider()

    # ----------------------
    # 3️⃣ Urbanité / ruralité
    # ----------------------
    st.header("3️⃣ Urbanité / ruralité en Occitanie")

    df_occ = df_merge[df_merge["departement"].isin(DEPARTEMENTS_OCCITANIE)]

    df_occ["departement_nom"] = (
    df_occ["departement"]
    .map(DEPARTEMENTS_NOMS)
    )

    fig_bar = px.bar(
    df_occ.sort_values("taux_total"),
    x="departement_nom",
    y="taux_total",
    color="urbanite_std",
    color_continuous_scale="RdBu"
    )
    fig_bar.update_layout(
    xaxis_title="Département",
    yaxis_title="Taux standardisé de mortalité (2023)"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.info(
        "On observe une tendance où plusieurs départements ruraux présentent des niveaux de mortalité élevés, mais la relation n’est pas systématique.\n"
        "Certains départements combinent d’autres facteurs structurels."
    )

    st.divider()

    