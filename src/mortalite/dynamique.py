import streamlit as st
from services.bigquery_client import run_query

@st.cache_data
def get_mortalite_historique(annee):
    query = f"""
    SELECT territoire, annee, taux_brut_pour_1000
    FROM `sante-et-territoires.sante.mortalite_nationale_historique`
    WHERE annee = {annee}
    """
    return run_query(query)

def render_dynamique():
    st.subheader("📈 Dynamique temporelle")

    annee = st.selectbox(
        "Choisir une année",
        list(range(2010, 2024)),
        index=13
    )

    df = get_mortalite_historique(annee)
    df = df.sort_values(by='taux_brut_pour_1000', ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Taux moyen",
            round(df["taux_brut_pour_1000"].mean(), 2)
        )

    with col2:
        st.metric(
            "Territoire le plus élevé",
            df.iloc[0]["territoire"]
        )

    st.dataframe(df)