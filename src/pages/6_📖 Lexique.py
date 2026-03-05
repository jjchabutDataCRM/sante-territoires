import streamlit as st
from pathlib import Path

try:
    BASE_DIR = Path(__file__).resolve().parent
except NameError:
    BASE_DIR = Path.cwd()

ROOT = BASE_DIR.parent
DATA_DIR = ROOT / "data"

path_md = DATA_DIR / 'lexique.md'

with open(path_md, "r", encoding="utf-8") as f:
        contenu_md = f.read()

st.markdown(contenu_md)