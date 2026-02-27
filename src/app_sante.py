import streamlit as st
import pandas as pd
from mortalite.mortalite import render

# ─── CONSTANTES ──────────────────────────────────────────────────────────────

DATA_DIR = '../data/processed'

COLOR_MAP = {
    'LightGreen':    "#a4f10a",
    'Green':   "#0dc735",
    'LightBlue': "#33c3f3",
    'Blue':   "#3194e6",
    'Purple':  "#a160cf",
    'Grey':   '#C2C5C6',
}

APL_COLS     = ['apl_medecins', 'apl_dentistes', 'apl_infirmiers', 'apl_kines', 'apl_sagesfemmes']
APL_STD_COLS = ['apl_medecins_std', 'apl_dentistes_std', 'apl_infirmiers_std', 'apl_kines_std', 'apl_sagesfemmes_std']
APL_LABELS   = ['Médecins', 'Dentistes', 'Infirmiers', 'Kinés', 'Sages-femmes']

def _sq(hex_color, size=13):
    return (f'<span style="display:inline-block;width:{size}px;height:{size}px;'
            f'background:{hex_color};border-radius:2px;vertical-align:middle;'
            f'margin-right:5px"></span>')

TYPE_LABELS = {
    'comm': 'Commune',
    'dept': 'Département',
    'epci': 'EPCI',
    'reg':  'Région',
    'ze':   "Zone d'emploi",
}


# ─── CONFIG PAGE ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Diagnostic Territorial Santé",
    page_icon="🩺",
    layout="wide"
)

# ─── CHARGEMENT DONNÉES ──────────────────────────────────────────────────────

@st.cache_data
def load_referentiel():
    return pd.dataframe
    # return pd.read_parquet(f'{DATA_DIR}/data/commune/score_sante_territoires_final.parquet')

# ─── HELPERS COULEUR ─────────────────────────────────────────────────────────

def hex_to_rgb(hex_color):
    h = hex_color.lstrip('#')
    return [int(h[i:i+2], 16) for i in (0, 2, 4)]

def get_fill_color(apl_val):
    if pd.isna(apl_val):
        return hex_to_rgb(COLOR_MAP['Purple']) + [80]
    elif apl_val < 2.5:
        return hex_to_rgb(COLOR_MAP['Blue'])  + [200]
    elif apl_val < 3.5:
        return hex_to_rgb(COLOR_MAP['LightBlue']) + [200]
    elif apl_val < 5.0:
        return hex_to_rgb(COLOR_MAP['Green']) + [200]
    else:
        return hex_to_rgb(COLOR_MAP['LightGreen']) + [200]

def get_color_hex(apl_val):
    if pd.isna(apl_val):   return COLOR_MAP['Grey']
    elif apl_val < 2.5:    return COLOR_MAP['Purple']
    elif apl_val < 3.5:    return COLOR_MAP['Blue']
    elif apl_val < 5.0:    return COLOR_MAP['Green']
    else:                  return COLOR_MAP['LightGreen']

def niveau_apl(apl_val):
    if pd.isna(apl_val):   return 'Inconnu'
    elif apl_val < 2.5:    return 'Critique'
    elif apl_val < 3.5:    return 'Faible'
    elif apl_val < 5.0:    return 'Moyen'
    else:                  return 'Bon'

# ─── CALCUL  ─────────────────────────────────────────────────────────


# ─── CALCUL APL ──────────────────────────────────────────────────────────────


# ─── CARTE PYDECK ─────────────────────────────────────────────────────────────


# ─── CARTE FOLIUM ─────────────────────────────────────────────────────────────



# ─── NAVIGATION ──────────────────────────────────────────────────────────────

pages = {"🏠 Accueil": "accueil",
         "🔧 Outil de Diagnostic": "diagnostic",
         "☠️ Mortalité":"mortalité",
         "🏢 Etablissements":"etablissement",
         "🏙️ Quartiers Prioritaires":"quartier",
         "🤒 Pathologies":"pathologie",
         "📜 Lexique":"lexique",
         "📖 Documentation":'documentation'
        }
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Navigation", list(pages.keys()), label_visibility="collapsed")

# ─── PAGE ACCUEIL ─────────────────────────────────────────────────────────────

if selection == "🏠 Accueil":
    st.title("🏥 Diagnostic Territorial de Santé Publique")
    st.markdown("""
    
    Cet outil permet de réaliser un diagnostic territorial de santé publique.

    ### Fonctionnalités


    ### Utilisation


    ---
    **Projet Open Data University - Challenge Fondation Roche**
    """)

# ─── PAGE DIAGNOSTIC ──────────────────────────────────────────────────────────

elif selection == "🔧 Outil de Diagnostic":
    st.title("🔧 Outil de Diagnostic Territorial")

    # ── Chargement des ressources ──────────────────────────────────────────


    # ── Configuration ────────────────────────────────────────────


    # ── Calcul ────────────────────────────────────────────────────────────
    
    
    # ── Affichage ────────────────────────────────────────────────────────────
    
elif selection == "☠️ Mortalité":
    render()
    # ── Chargement des ressources ──────────────────────────────────────────


    # ── Configuration ────────────────────────────────────────────


    # ── Calcul ────────────────────────────────────────────────────────────
    
    
    # ── Affichage ────────────────────────────────────────────────────────────
    
elif selection == "🏢 Etablissements":
    st.title("🏢 Etablissements")
    # ── Chargement des ressources ──────────────────────────────────────────


    # ── Configuration ────────────────────────────────────────────


    # ── Calcul ────────────────────────────────────────────────────────────
    
    
    # ── Affichage ────────────────────────────────────────────────────────────
    
elif selection == "🏙️ Quartiers Prioritaires":
    st.title("🏙️ Quartiers Prioritaires")
    # ── Chargement des ressources ──────────────────────────────────────────


    # ── Configuration ────────────────────────────────────────────


    # ── Calcul ────────────────────────────────────────────────────────────
    
    
    # ── Affichage ────────────────────────────────────────────────────────────
    
elif selection == "🤒 Pathologies":
    st.title("🤒 Pathologies")
    # ── Chargement des ressources ──────────────────────────────────────────


    # ── Configuration ────────────────────────────────────────────


    # ── Calcul ────────────────────────────────────────────────────────────
    
    
    # ── Affichage ────────────────────────────────────────────────────────────
    
elif selection == "📜 Lexique":
    st.title("📜 Lexique")
    st.markdown("""
                ...
                """)
elif selection == "📖 Documentation":
    st.title("📖 Documentation")
    st.markdown("""
📋 Score APL - Méthodologie
Score composite d'accessibilité aux soins primaires calculé comme suit :

text
score_apl = 0.35xAPL_médecins_std + 0.25xAPL_infirmiers_std + 
            0.20xAPL_kines_std + 0.15xAPL_dentistes_std + 
            0.05xAPL_sages-femmes_std

Standardisation : score Z sur chaque APL pour comparabilité

Score Z : (APL - moyenne France) / écart-type France
z > 0 = offre supérieure moyenne nationale
Source : StandardScaler sklearn

Pondération : Priorité médecins généralistes (35%) puis infirmiers (25%) selon impact population [Drees]

Quintiles : Q1 (très faible) à Q5 (très bon) - moyenne France = Q3

Référence : DREES/IRDES - APL Méthodologie 2020
https://drees.solidarites-sante.gouv.fr/sources-outils-et-enquetes/lindicateur-daccessibilite-potentielle-localisee-apl


Interprétation : Q1+Q2 = priorités implantation (déserts médicaux)
    """)