import streamlit as st
import pandas as pd
import plotly.express as px
#from services.bigquery_client import run_query

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

@st.cache_data
def get_intensite_globale():

    # ---------------------------
    # Chargement local
    # ---------------------------
    df = pd.read_csv("data/processed/mortalite_2023_standardise_all.csv")

    df = (
        df[df["annee"] == 2023]
        .query("sexe == 'Tous sexes'")
        .groupby("departement", as_index=False)["valeur"]
        .sum()
        .rename(columns={"valeur": "taux_total"})
    )

    df["ecart_a_moyenne"] = (
        df["taux_total"] - df["taux_total"].mean()
    ).round(2)

    return df

    # ---------------------------
    # BigQuery (désactivé)
    # ---------------------------
    """
    query = '''
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
    '''
    return run_query(query)
    """

# ===============================
# 2. Rendu Streamlit
# ===============================
def render_diagnostic():

    df = get_intensite_globale()

        # Remplacement des codes départements par les noms
    df["departement_nom"] = (
        df["departement"]
        .astype(str)
        .map(DEPARTEMENTS_NOMS)
        .fillna(df["departement"])
    )

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
        y="departement_nom",
        orientation="h",
        template="plotly_white",
        labels={
            "taux_total": "Décès pour 100 000 habitants",
            "departement_nom": "Département"
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

    st.header("3️⃣ Position de la Haute-Garonne en Occitanie")

    df_occitanie = df[df["departement"].isin(DEPARTEMENTS_OCCITANIE)].copy()

    # Marquer Haute-Garonne
    df_occitanie["Focus"] = df_occitanie["departement"].apply(
        lambda x: "Haute-Garonne" if x == "31" else "Autres départements"
    )

    fig_dot = px.scatter(
        df_occitanie,
        x="taux_total",
        y=["Occitanie"] * len(df_occitanie),  # tous sur une seule ligne
        color="Focus",
        size=df_occitanie["Focus"].apply(lambda x: 14 if x == "Haute-Garonne" else 8),
        color_discrete_map={
            "Haute-Garonne": "#FF7F0E",
            "Autres départements": "#B0B0B0"
        },
        template="plotly_white",
        labels={"taux_total": "Décès pour 100 000 habitants"}
    )

    # Ligne moyenne régionale
    fig_dot.add_vline(
        x=moyenne_occitanie,
        line_width=2,
        line_color="black"
    )

    fig_dot.add_annotation(
        x=moyenne_occitanie,
        y=1,
        yref="paper",
        text="Moyenne régionale",
        showarrow=False
    )

    fig_dot.update_yaxes(showticklabels=False)

    st.plotly_chart(fig_dot, use_container_width=True)

    val_31 = df[df["departement"] == "31"]["taux_total"].values[0]

    ecart_fr = val_31 - moyenne_france
    ecart_occ = val_31 - moyenne_occitanie

    direction_fr = "au-dessus" if ecart_fr > 0 else "en dessous"
    direction_occ = "au-dessus" if ecart_occ > 0 else "en dessous"

    st.info(f"La Haute-Garonne présente un taux de **{round(val_31,1)} décès pour 100 000 habitants**.")

    st.markdown(f"""
    • Soit **{abs(round(ecart_fr,1))} décès pour 100 000 habitants {direction_fr}** de la moyenne nationale  
    • Et **{abs(round(ecart_occ,1))} décès pour 100 000 habitants {direction_occ}** de la moyenne régionale
    """)

    st.divider()

    