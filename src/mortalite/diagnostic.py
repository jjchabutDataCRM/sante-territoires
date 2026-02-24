import streamlit as st
import pandas as pd
import plotly.express as px
from services.bigquery_client import run_query

DEPARTEMENTS_OCCITANIE = [
    "09","11","12","30","31","32","34",
    "46","48","65","66","81","82"
]

DEPARTEMENTS_NOMS = {
    "971": "Guadeloupe",
    "972": "Martinique",
    "973": "Guyane",
    "974": "La Réunion",
    "976": "Mayotte",
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

# ===============================
# 1. Requête BigQuery
# ===============================
@st.cache_data
def get_intensite_globale():
    query = """
    SELECT
        departement,
        SUM(valeur) AS taux_total,
        ROUND(
            SUM(valeur) - AVG(SUM(valeur)) OVER(),
            2
        ) AS ecart_a_moyenne
    FROM `sante-et-territoires.sante.mortalite_2023_standardise_all`
    WHERE annee = 2023
      AND sexe = 'Tous sexes'
    GROUP BY departement
    ORDER BY taux_total DESC
    """
    return run_query(query)

# ===============================
# 2. Rendu Streamlit
# ===============================
def render_diagnostic():

    df = get_intensite_globale()

    if df.empty:
        st.warning("Aucune donnée trouvée.")
        return

    # ======================
    # TITRE
    # ======================
    st.title("📊 Diagnostic territorial 2023")

    st.markdown("""
    Le taux standardisé de mortalité constitue un indicateur synthétique
    permettant d'identifier d'éventuels déséquilibres territoriaux.
    """)

    st.divider()

    # ======================
# 1️⃣ POSITION DE L’OCCITANIE
# ======================

    st.header("1️⃣ Position de l’Occitanie")

    # ---- Calcul des moyennes ----
    moyenne_france = df["taux_total"].mean()

    df_occitanie = df[df["departement"].isin(DEPARTEMENTS_OCCITANIE)]
    moyenne_occitanie = df_occitanie["taux_total"].mean()

    ecart_reg = moyenne_occitanie - moyenne_france

    # ---- Affichage KPI ----
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Moyenne France",
            value=f"{round(moyenne_france,1)} décès / 100 000"
        )

    with col2:
        st.metric(
            label="Moyenne Occitanie",
            value=f"{round(moyenne_occitanie,1)} décès / 100 000",
            delta=round(ecart_reg,1)
        )

    # ---- Interprétation ----
    if ecart_reg < 0:
        st.info(
            f"L’Occitanie se situe **{abs(round(ecart_reg,1))} points en dessous** de la moyenne nationale."
        )
    else:
        st.warning(
            f"L’Occitanie se situe **{round(ecart_reg,1)} points au-dessus** de la moyenne nationale."
        )

    st.divider()

    # ======================
    # 2️⃣ CLASSEMENT REGIONAL
    # ======================

    st.header("2️⃣ Les écarts territoriaux sont-ils significatifs ?")

    df_occitanie = df[df["departement"].isin(DEPARTEMENTS_OCCITANIE)]
    df_occitanie_sorted = df_occitanie.sort_values("taux_total")

    fig_occ = px.bar(
        df_occitanie_sorted,
        x="taux_total",
        y="departement",
        orientation="h",
        template="plotly_white",
        labels={
            "taux_total": "Décès pour 100 000 habitants",
            "departement": "Département"
        },
        title="Taux standardisé de mortalité – Occitanie 2023"
    )

    fig_occ.add_vline(
        x=moyenne_occitanie,
        line_color="black",
        line_width=2
    )

    fig_occ.add_annotation(
    x=moyenne_occitanie,
    y=1.05,
    yref="paper",
    text="Moyenne régionale",
    showarrow=False,
    font=dict(size=12, color="black"),
    xanchor="center"
    )

    st.plotly_chart(fig_occ, use_container_width=True)

    st.info(
    "Les départements d’Occitanie présentent des écarts mesurés autour de la moyenne régionale. "
    "La dispersion reste limitée, mais certains territoires se situent durablement au-dessus ou en dessous de la moyenne, "
    "ce qui peut orienter la priorisation des politiques de prévention et d’accès aux soins."
    )  

    st.divider()

    # ======================
    # 3️⃣ FOCUS HAUTE-GARONNE
    # ======================

    st.header("3️⃣ Focus Haute-Garonne (31)")

    val_31 = df[df["departement"] == "31"]["taux_total"].values[0]

    ecart_fr = val_31 - moyenne_france
    ecart_occ = val_31 - moyenne_occitanie

    st.markdown(f"""
    La Haute-Garonne présente un taux de
    **{round(val_31,1)} décès pour 100 000 habitants**.

    • Écart à la moyenne nationale : **{round(ecart_fr,1)} points**  
    • Écart à la moyenne régionale : **{round(ecart_occ,1)} points**
    """)

    st.divider()

    