import streamlit as st
import sys
import os

# Menambahkan path agar module dapat ditemukan
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# PENTING: Impor ini harus ada agar pickle mengenali objek WordVocab
from vocabulary import WordVocab


from i18n import TEXTS
st.set_page_config(page_title="Restorasi Naskah Sunda Kuno", layout="wide")
from ui.home import show_home
from ui.restoration import show_restoration



LANGUAGES = {"Indonesia": ["Beranda", "Restorasi"],
             "English":   ["Home",    "Restoration"]}

st.sidebar.title("Menu Navigasi")
language = st.sidebar.selectbox("Pilih Bahasa / Select Language",
                                list(LANGUAGES.keys()), index=0)
page = st.sidebar.radio("Menu", LANGUAGES[language], index=0)

if page in ("Beranda", "Home"):
    show_home(language)
else:
    show_restoration(language)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("© 2025 Restorasi Naskah Sunda Kuno")
