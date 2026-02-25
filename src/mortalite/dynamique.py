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
    Cette section analyse l’évolution des taux standardisés de mortalité
    entre 2010 et 2023 afin d’identifier les tendances longues,
    les ruptures et les éventuelles divergences territoriales.
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
        color_discrete_sequence=["#2E5AF9", "#E4572E"],
        labels={
            "valeur": "Taux standardisé (pour 100 000)",
            "annee": "Année"
        }
    )

    fig = style_fig(fig)

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "L’Occitanie présente une tendance à la baisse plus marquée que la France, "
        "notamment entre 2010 et 2015. Cependant, les deux territoires connaissent une hausse significative en 2020–2021, "
        "cohérente avec le choc sanitaire de la pandémie de COVID-19."
    )

    st.divider()

    # ----------------------
    # Analyse du choc 2020 par département
    # ----------------------

    st.header("Amplitude du choc 2020 par département en Occitanie")

    df_dept = df[
        (df["cause"] == "Toutes causes") &
        (df["sexe"] == "Tous sexes") &
        (df["departement"].isin(DEPARTEMENTS_OCCITANIE))
    ]

    # moyenne 2015–2019
    moy_pre = (
        df_dept[df_dept["annee"].between(2015, 2019)]
        .groupby("departement")["valeur"]
        .mean()
        .reset_index()
        .rename(columns={"valeur": "moy_pre_covid"})
    )

    # valeur 2020
    val_2020 = (
        df_dept[df_dept["annee"] == 2020]
        .groupby("departement")["valeur"]
        .mean()
        .reset_index()
        .rename(columns={"valeur": "val_2020"})
    )

    df_choc = moy_pre.merge(val_2020, on="departement")
    df_choc["ecart_2020"] = df_choc["val_2020"] - df_choc["moy_pre_covid"]
    df_choc["departement_nom"] = df_choc["departement"].map(DEPARTEMENTS_NOMS)

    fig_choc = px.bar(
        df_choc.sort_values("ecart_2020", ascending=False),
        x="departement_nom",
        y="ecart_2020",
        template="simple_white",
        labels={
            "departement_nom": "Département",
            "ecart_2020": "Surmortalité 2020 vs 2015–2019"
        }
    )

    st.plotly_chart(fig_choc, use_container_width=True)

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
    color_discrete_sequence=["#4C78A8", "#F58518", "#54A24B"],
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
        "Les maladies de l’appareil circulatoire présentent une baisse structurelle sur la période. "
        "Les maladies respiratoires connaissent une hausse marquée en 2020–2021, "
        "cohérente avec le choc sanitaire."
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
        facet_row="cause",
        markers=True,
         template="simple_white",
        color_discrete_sequence=["#3B82F6", "#EF4444"],
        labels={
            "valeur": "Taux standardisé (pour 100 000)",
            "annee": "Année",
            "sexe": "Sexe",
            "cause": ""
        }
    )

    fig_sexe.update_traces(line=dict(width=3))
    fig_sexe.update_layout(
        height=850,
        font=dict(family="Inter, sans-serif", size=13),
        margin=dict(l=20, r=120, t=40, b=20),
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
        "Les hommes présentent des taux de mortalité plus élevés que les femmes pour les trois grandes causes, avec un écart particulièrement marqué pour les maladies de l’appareil circulatoire. "
        "Cependant, les tendances temporelles sont similaires entre les sexes."
    )

    st.divider()
     