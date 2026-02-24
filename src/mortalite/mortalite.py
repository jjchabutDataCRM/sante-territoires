import streamlit as st
from mortalite.diagnostic import render_diagnostic
from mortalite.dynamique import render_dynamique
from mortalite.croisement import render_croisement

def render():
    st.title("☠️ Mortalité")

    tab1, tab2, tab3 = st.tabs([
        "📊 Diagnostic 2023",
        "📈 Dynamique 2010–2023",
        "🔗 Croisement avec l'offre"
    ])

    with tab1:
        render_diagnostic()

    with tab2:
        render_dynamique()

    with tab3:
        render_croisement()
