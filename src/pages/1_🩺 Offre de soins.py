import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
#from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from pathlib import Path
import numpy as np
#import os
import folium
from streamlit_folium import st_folium
import seaborn as sns

# On essaie d'utiliser __file__, sinon on prend le dossier actuel
try:
    BASE_DIR = Path(__file__).resolve().parent
except NameError:
    BASE_DIR = Path.cwd()

ROOT = BASE_DIR.parent
DATA_DIR = ROOT / "data"


# --- CONFIGURATION ---
st.set_page_config(page_title="Offres de soins - Occitanie", layout="wide")

# --- CHARGEMENT DES DONNÉES ---
# Assurez-vous que df_geom_epci et df_geom_reg sont accessibles ici
@st.cache_data
def load_geom():

    df_geom_epci = gpd.read_parquet(DATA_DIR / 'epci_geom_simplified.parquet')
    df_geom_reg = gpd.read_parquet(DATA_DIR / 'regions_geom_simplified.parquet')
    
    return df_geom_epci, df_geom_reg

@st.cache_data
def load_data():
    
    df_apl = pd.read_parquet(DATA_DIR / 'final_comm_indic_projet.parquet')
    
    cols_to_weight = [
    'apl_medecins', 'apl_dentistes', 'apl_infirmiers', 'apl_kines', 
    'apl_sagesfemmes', 'delta_apl_medecins', 'delta_apl_dentistes', 
    'delta_apl_infirmiers', 'delta_apl_kines', 'delta_apl_sagesfemmes', 
    'apl_medecins_std', 'apl_dentistes_std', 'apl_infirmiers_std', 
    'apl_kines_std', 'apl_sagesfemmes_std', 
    'tx_mort_premature_std', 'tps_SU_SMUR_std'
    ]

    # Calcul de la moyenne pondérée
    # On multiplie le DataFrame des colonnes par la série population
    # weighted_sums = df_apl[cols_to_weight].multiply(df_apl['population'], axis=0).sum()
    # total_population = df_apl['population'].sum()
    # stats_france = weighted_sums / total_population
    # 
    stats_france = get_weighted_means(df_apl, cols_to_weight)
    
    # Région occitanie 
    df_occitanie = df_apl[df_apl['code_insee_de_la_region'] == '76'].copy()
    # Calcul pour la région
    stats_occitanie = get_weighted_means(df_occitanie, cols_to_weight)
    
    siren_epci_1 = "243100518" # Agglo Toulouse
    siren_epci_2 = "200043776"  # Pyrénées Audoises

    # Calculs
    stats_epci_1 = get_weighted_means(df_occitanie[df_occitanie['codes_siren_des_epci'] == siren_epci_1], cols_to_weight)
    stats_epci_2 = get_weighted_means(df_occitanie[df_occitanie['codes_siren_des_epci'] == siren_epci_2], cols_to_weight)

    # Assemblage du tableau comparatif
    comparaison = pd.DataFrame({
        'Occitanie': stats_occitanie,
        'Toulouse': stats_epci_1,
        'Pyrénées_Audoises': stats_epci_2,
        'France': stats_france
    })

    # Ajout d'une colonne d'écart en %
    comparaison['Ecart Toulouse / Région (%)'] = ((comparaison['Toulouse'] - comparaison['Occitanie']) / comparaison['Occitanie']) * 100
    comparaison['Ecart Pyr Audoises / Région (%)'] = ((comparaison['Pyrénées_Audoises'] - comparaison['Occitanie']) / comparaison['Occitanie']) * 100
    comparaison['Ecart Toulouse / Pyr Audoises (%)'] = ((comparaison['Toulouse'] - comparaison['Pyrénées_Audoises']) / comparaison['Toulouse']) * 100

    
    return df_occitanie, comparaison

def get_weighted_means(dataframe, columns, weight_col='population'):
    """Calcule la moyenne pondérée pour une liste de colonnes."""
    results = {}
    for col in columns:
        # On ignore les lignes où la donnée est manquante (NaN)
        valid_mask = dataframe[col].notna()
        df_valid = dataframe[valid_mask]
        
        if not df_valid.empty:
            weighted_sum = (df_valid[col] * df_valid[weight_col]).sum()
            total_pop = df_valid[weight_col].sum()
            results[col] = weighted_sum / total_pop
        else:
            results[col] = None
    return pd.Series(results)

# --- INTERFACE ---
st.title("📂 Analyse de l'Offre de Soins")

# Création des 3 onglets
tab_carte, tab_histo, tab_radar, tab_table, tab_repartition, tab_methodo = st.tabs(["📍 Carte", "📊 APL", "🕸️ Multi Facteurs", "📋 Tableaux (détails)", "🗂️ Répartition", "ℹ️ Méthodologie"])

# --- ONGLET 1 : CARTE ---
with tab_carte:
    st.subheader("Contexte Géographique : Relief et Littoral")
    
    df_geom_epci, df_geom_reg = load_geom()
    
# 1. Récupération de la ligne de la région Occitanie
    region_occ = df_geom_reg[df_geom_reg['code_siren'] == '200053791']
    
    if not region_occ.empty:
        # Utilisation directe des colonnes lon et lat du fichier
        occ_center = [region_occ['lat'].iloc[0], region_occ['lon'].iloc[0]]
        
        # Initialisation de la carte avec le centre du fichier
        m = folium.Map(
            location=occ_center, 
            zoom_start=7, 
            tiles="OpenStreetMap",
            control_scale=True
        )

        # 2. Ajout des polygones (GeoJson)
        # Contour Région
        folium.GeoJson(
            region_occ,
            style_function=lambda x: {'fillColor': 'none', 'color': '#333333', 'weight': 3}
        ).add_to(m)

        # EPCI Cibles
        cibles_info = {
            '243100518': {'nom': 'Toulouse Métropole', 'color': '#1f77b4'},
            '200043776': {'nom': 'CC des Pyrénées Audoises', 'color': '#ff7f0e'}
        }
        
        # --- Dans votre boucle d'affichage des EPCI cibles ---

        for siren, info in cibles_info.items():
            subset = df_geom_epci[df_geom_epci['code_siren'] == siren]
            
            if not subset.empty:
                # 1. Dessiner le polygone
                folium.GeoJson(
                    subset,
                    style_function=lambda x, color=info['color']: {
                        'fillColor': color, 'color': 'black', 'weight': 2, 'fillOpacity': 0.6
                    },
                    tooltip=info['nom']
                ).add_to(m)
        
                # 2. Ajouter l'étiquette de texte fixe (Uniquement pour l'Aude ou les deux)
                # On récupère lon/lat directement de votre fichier
                folium.map.Marker(
                    location=[subset['lat'].iloc[0], subset['lon'].iloc[0]],
                    icon=folium.DivIcon(
                    html=f"""<div style="
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        color: #333;
                        font-weight: bold;
                        font-size: 11px;
                        background-color: rgba(255, 255, 255, 0.8);
                        border: 1px solid #999;
                        border-radius: 3px;
                        padding: 2px 5px;
                        white-space: nowrap;
                        text-align: center;
                        ">
                            {info['nom']}
                            </div>""",
                        icon_anchor=(50, 0) # Ajuste le décalage pour centrer le texte
                    )
                ).add_to(m)
        
        # 3. Ajustement automatique aux limites (pour ne pas voir toute la France)
        # On définit les coins Sud-Ouest et Nord-Est à partir de la géométrie
        bounds = region_occ.geometry.total_bounds # [minx, miny, maxx, maxy]
        m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

        # 4. Affichage Streamlit (syntaxe 2026)
        st_folium(m, width='stretch', height=600, returned_objects=[])

    else:
        st.warning("Données de la région Occitanie non trouvées.")
    
    st.caption("""
        La comparaison de Toulouse Métropole avec la CC des Pyrénées Audoises incarne les contrastes structurels de la région Occitanie. 
        Elle met en exergue le 'grand écart' territorial entre un pôle urbain hyper-connecté, porté par une dynamique démographique soutenue, 
        et un espace rural de faible densité dont l'accès aux infrastructures de santé est conditionné par l'enclavement géographique et les contraintes du relief pyrénéen.
    """)

# --- ONGLET 2 : GRAPHIQUES ---
with tab_histo:
    st.subheader("Acessibilioté aux soins")
    df_occitanie, df_comparaison = load_data()
    
    # 1. Préparation des données 
    cols_etude = ['apl_medecins_std', 'apl_dentistes_std', 'apl_infirmiers_std', 
                  'apl_kines_std', 'apl_sagesfemmes_std']
    #selected_cols = st.multiselect("Indicateurs à afficher", options=cols_etude, default=cols_etude)
    df_plot = df_comparaison.loc[cols_etude, ['Pyrénées_Audoises', 'Toulouse', 'Occitanie', 'France']]

    # 2. Création de la figure Streamlit
    st.title("Analyse de l'offre de soins")
    st.subheader("Comparaison de l'accessibilité (APL)")

    # Utilisation explicite de l'objet figure pour éviter les avertissements Streamlit
    fig, ax = plt.subplots(figsize=(10, 6))

    labels_propres = [label.replace('_std', '').replace('apl_', '').capitalize() for label in cols_etude]
    
    df_plot.plot(kind='bar', ax=ax, rot=45)

    ax.set_title("Comparaison de l'accessibilité aux soins")
    ax.set_ylabel("Indicateur APL")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_xticks(range(len(labels_propres)))
    ax.set_xticklabels(labels_propres)
    
    # 3. Affichage dans Streamlit
    st.pyplot(fig)
    
    st.subheader("💡 Analyse de l'accessibilité")

    # Utilisation de colonnes pour une mise en page aérée
    col_analysis_1, col_analysis_2 = st.columns(2)

    with col_analysis_1:
        st.markdown("### 🌆 Pôles Urbains")
        st.info(
            "**Toulouse** présente une concentration de spécialistes (Dentistes, Kinés) "
            "très au-dessus de la moyenne régionale, illustrant l'attractivité des zones "
            "urbaines pour les professions libérales."
        )

    with col_analysis_2:
        st.markdown("### 🌲 Zones Rurales")
        st.warning(
            "Dans les **Pyrénées Audoises**, le déficit est particulièrement visible sur "
            "les professions de premier recours (Médecins). Cependant, on note une "
            "relative résilience sur les **Infirmiers**, qui constituent souvent le "
            "dernier rempart de proximité."
        )

    # Section de synthèse régionale
    with st.expander("🔍 Zoom sur la dynamique régionale (Occitanie vs France)"):
        st.write(
            "L'**Occitanie** se positionne systématiquement au-dessus de la moyenne nationale "
            "sur tous les indicateurs APL affichés. Cela démontre que la problématique "
            "régionale n'est pas un manque global de moyens, mais une **inégalité de "
            "répartition interne** flagrante."
        )

with tab_radar:
    st.header("Analyse Multidimensionnelle")
    
    df_occitanie, comparaison = load_data()
    
    st.write("Ce graphique radar permet de visualiser simultanément l'offre de soins et les indicateurs de risques.")

    # 1. Préparation des données (on utilise les colonnes que tu as définies)
    labels = ['apl_medecins_std', 'apl_dentistes_std', 'apl_infirmiers_std', 'apl_kines_std', 'tx_mort_premature_std','tps_SU_SMUR_std']

    # Extraction des valeurs
    stats_toulouse = comparaison.loc[labels, 'Toulouse'].values
    stats_pyr = comparaison.loc[labels, 'Pyrénées_Audoises'].values
    stats_occ = comparaison.loc[labels, 'Occitanie'].values
    stats_france = comparaison.loc[labels, 'France'].values

    # 2. Configuration des angles et fermeture de la boucle
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()

    stats_toulouse = np.append(stats_toulouse, stats_toulouse[0])
    stats_pyr = np.append(stats_pyr, stats_pyr[0])
    stats_occ = np.append(stats_occ, stats_occ[0])
    stats_france = np.append(stats_france, stats_france[0])
    angles = np.append(angles, angles[0])

    # 3. Création du graphique avec Matplotlib
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Tracé des lignes
    ax.plot(angles, stats_toulouse, color='#1f77b4', linewidth=2, label='Toulouse', marker='o')
    ax.plot(angles, stats_pyr, color='#ff7f0e', linewidth=2, label='Pyr. Audoises', marker='s')
    ax.plot(angles, stats_occ, color='gray', linewidth=2, linestyle='--', label='Occitanie', marker='x')
    ax.plot(angles, stats_france, color='black', linewidth=1.5, label='France', alpha=0.6)

    # Remplissage de la zone France (moyenne)
    ax.fill(angles, stats_france, color='gray', alpha=0.10)

    # 4. Habillage
    ax.set_xticks(angles[:-1])
    clean_labels = [l.replace('_std', '').replace('apl_', '').replace('_', ' ').title() for l in labels]
    ax.set_xticklabels(clean_labels)

    # Ajustement dynamique des limites pour éviter que le radar sorte du cadre
    ax.set_ylim(min(stats_pyr.min(), stats_toulouse.min()) - 0.5, 
                max(stats_pyr.max(), stats_toulouse.max()) + 0.5)

    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.title("Profil Santé Standardisé : Comparaison Territoriale", pad=20)

    # 5. Affichage dans Streamlit
    st.pyplot(fig)

    # --- Ajout des commentaires interprétatifs en dessous ---
    with st.expander("💡 Guide de lecture"):
        st.markdown("""
        ### 💡 Guide de lecture
        * **Le centre du radar (-2 / -1)** : Représente une sous-performance ou un risque faible.
        * **Le cercle grisé (0)** : Représente la **moyenne nationale**.
        * **Points vers l'extérieur** : 
            * Sur les axes **Soins** (Médecins, etc.) = Bonne dotation.
            * Sur les axes **Risques** (Mortalité, SMUR) = **Fragilité accrue**.
        """)
    st.divider()

    st.subheader("Analyse   ")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 🚩 Points d'Alerte")
        st.error("- **Désertification ciblée :** Le déficit en médecins généralistes dans les zones rurales est critique.\n- **Insécurité Sanitaire :** Forte corrélation visuelle entre l'éloignement des urgences (SMUR) et la surmortalité prématurée.")

    with col_b:
        st.markdown("#### ✅ Points de Force")
        st.success("- **Maillage Infirmier :** Une présence maintenue qui stabilise les territoires fragiles.\n- **Attractivité Régionale :** L'Occitanie reste globalement mieux dotée que la moyenne nationale.")

    with st.expander("📝 Conclusion stratégique"):
        st.info("L'analyse démontre que la politique de santé ne doit pas viser une augmentation globale du nombre de soignants en Occitanie, mais une **réorientation prioritaire** vers les zones de 'double peine' identifiées par le radar (zones à faible APL et fort temps SMUR).")

    with tab_table:

        def color_negative_red(val):
            if isinstance(val, (int, float)):
                color = '#ef5350' if val < 0 else '#66bb6a' # Rouge/Vert plus doux
                return f'color: {color}; font-weight: bold'
            return ''

        st.subheader("Tableau comparatif des écarts")

        # 1. Sélection des colonnes cibles
        subset_cols = [
            'Ecart Toulouse / Région (%)', 
            'Ecart Pyr Audoises / Région (%)', 
            'Ecart Toulouse / Pyr Audoises (%)'
        ]

        # 2. Application du style 
        
        noms_courts = {
            "Ecart Toulouse / Région (%)": "Tlse / Rég",
            "Ecart Pyr Audoises / Région (%)": "Pyr.Aud./ Rég",
            "Ecart Toulouse / Pyr Audoises (%)": "Tlse / Pyr.Aud."
        }
        
        styled_df = comparaison.style.map(color_negative_red, subset=subset_cols)\
            .format("{:.1f}%", subset=subset_cols) # Ajoute le symbole % proprement

        # 3. Affichage dans Streamlit
        st.dataframe(styled_df,
                     column_config={
                        col: st.column_config.Column(noms_courts.get(col, col), width="medium")
                        for col in comparaison.columns
                    },
                     use_container_width=True)
with tab_repartition:
    df_occitanie, combinaison = load_data()
    st.subheader("Profil de distribution des risques")
    
    df_violin = df_occitanie.melt(
    value_vars=['tps_SU_SMUR_std', 'tx_mort_premature_std'],
    var_name='Indicateur',
    value_name='Z-Score'
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.violinplot(
        data=df_violin, 
        x='Z-Score', 
        y='Indicateur', 
        inner="quart", 
        palette="Pastel1",
        bw_adjust=.5,
        ax=ax
    )
    ax.axvline(0, color='red', linestyle='--', alpha=0.5)
    ax.set_yticklabels(['Temps SMUR', 'Mortalité Prématurée'])
    ax.set_xlabel("Écart à la moyenne (Z-Score)")

    st.pyplot(fig)

    # --- 2. ANALYSE INTERPRÉTATIVE ---
    col1, col2 = st.columns(2)

    with col1:
        st.info("**Analyse du Temps SMUR**")
        st.write("""
        - **Forte dispersion** : Le violon s'étire jusqu'à +5, indiquant des inégalités d'accès majeures.
        - **La 'Traîne'** : La pointe fine à droite représente les communes en isolement extrême, comme les Pyrénées Audoises.
        """)

    with col2:
        st.info("**Analyse de la Mortalité**")
        st.write("""
        - **Profil Multimodal** : Les multiples "bosses" suggèrent des groupes de communes avec des réalités de santé très différentes.
        - **Plus compact** : Les écarts de mortalité sont moins extrêmes que les écarts de distance aux soins.
        """)
    
with tab_methodo:
    st.subheader("Méthodologie")
    st.markdown('''
### Limite liée au référentiel communal

Les données d’accessibilité aux professionnels de santé (APL) utilisées dans l’analyse correspondent au millésime 2023, tandis que le référentiel communal utilisé pour la cartographie repose sur la structure administrative la plus récente.

Certaines communes ayant connu des fusions ou modifications administratives peuvent donc présenter des écarts de correspondance. Ces cas restent marginaux et n’affectent pas significativement les tendances générales observées.
''')
    