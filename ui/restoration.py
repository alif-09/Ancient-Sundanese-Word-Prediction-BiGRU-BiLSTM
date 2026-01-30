import streamlit as st
import pandas as pd
import re
from predictor import WordPredictor
from i18n import TEXTS

def show_restoration(language: str):
    # Mengambil kamus bahasa yang sesuai
    t = TEXTS.get(language, TEXTS["Indonesia"])
    
    st.title(f"🏛️ {t['nav_restoration']}")

    # CSS Khusus (Tetap sama)
    st.markdown("""
    <style>
    div.stButton > button {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 0px !important;
        padding: 10px !important;
        text-align: left !important;
        background-color: #1f2227 !important;
        color: #e5e7eb !important;
        margin-bottom: -1px !important;
        display: flex !important;
        justify-content: space-between !important;
    }
    div.stButton > button[kind="primary"] {
        background-color: #ef4444 !important;
        color: white !important;
        border: 1px solid #ef4444 !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover {
        border-color: #ef4444 !important;
        background-color: #2b2e34 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    @st.cache_resource
    def load_predictor():
        return WordPredictor(folder_path="models")
    
    try:
        predictor = load_predictor()
    except Exception as e:
        st.error(f"Error: {e}")
        return

    # --- Sidebar Menggunakan Kamus ---
    st.sidebar.header(t["model_options"])
    model_choice = st.sidebar.radio(t["architecture"], ("Bi-GRU", "Bi-LSTM"))
    model_key = 'gru' if "GRU" in model_choice else 'lstm'

    # --- Area Input Menggunakan Kamus ---
    st.subheader(t["input_header"])
    input_text = st.text_area(t["restoration_hint"], 
                              value="teka rehe teka sirep [mask] harengo para botoh seok jadi mata", height=100)

    if 'multi_results' not in st.session_state:
        st.session_state.multi_results = None
    if 'selections' not in st.session_state:
        st.session_state.selections = {}

    if st.button(t["predict_button"], type="secondary", use_container_width=True):
        if "[mask]" in input_text.lower():
            with st.spinner("Analyzing..." if language == "English" else "Menganalisis..."):
                st.session_state.multi_results = predictor.predict_all_masks(input_text, model_key)
                st.session_state.selections = {i: 0 for i in range(len(st.session_state.multi_results))}
        else:
            st.warning("Token [mask] not found." if language == "English" else "Token [mask] tidak ditemukan.")

    # --- Tampilan Tabel dengan Kamus ---
    if st.session_state.multi_results:
        num_masks = len(st.session_state.multi_results)
        st.markdown("---")
        st.write(f"### {t['table_title']}")
        
        cols = st.columns(num_masks)
        
        for i, res in enumerate(st.session_state.multi_results):
            with cols[i]:
                st.markdown(f"<div style='text-align:center; font-weight:bold; background:#38404a; padding:5px;'>{'MASK' if language == 'English' else 'RUMPANG'} #{i+1}</div>", unsafe_allow_html=True)
                
                # Header kolom tabel
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; padding:5px 10px; color:#9ca3af; font-size:0.75rem; font-weight:bold; border-bottom:1px solid #38404a;'>
                    <span>{'WORD' if language == 'English' else 'KATA'}</span>
                    <span>{'SCORE' if language == 'English' else 'SKOR'}</span>
                </div>
                """, unsafe_allow_html=True)
                
                for idx, cand in enumerate(res['candidates']):
                    word = cand['word']
                    score = f"{cand['confidence']*100:.1f}%"
                    is_active = (st.session_state.selections.get(i) == idx)
                    display_label = f"{'✅ ' if is_active else ''}{word.ljust(15)} {score.rjust(10)}"
                    
                    if st.button(display_label, key=f"row_{i}_{idx}", use_container_width=True, 
                                 type="primary" if is_active else "secondary"):
                        st.session_state.selections[i] = idx
                        st.rerun()

        # --- Hasil Kalimat Menggunakan Kamus ---
        words_ui = input_text.split()
        words_plain = input_text.split()
        m_idx = 0
        for idx, w in enumerate(words_ui):
            if "[mask]" in w.lower() and m_idx < len(st.session_state.multi_results):
                sel_pos = st.session_state.selections.get(m_idx, 0)
                chosen = st.session_state.multi_results[m_idx]['candidates'][sel_pos]['word']
                words_ui[idx] = f":red[**{chosen}**]"
                words_plain[idx] = chosen
                m_idx += 1
        
        st.markdown("---")
        st.info(f"**{t['results_header']}**")
        st.markdown(f"#### {' '.join(words_ui)}")

        # --- Download Menggunakan Kamus ---
        download_text = f"input: {input_text}\noutput: {' '.join(words_plain)}"
        st.download_button(label=t["download_label"], data=download_text, 
                           file_name="restorasi_sunda.txt", mime="text/plain")

    # with st.expander("Methodology" if language == "English" else "Metodologi"):
    #     st.write(t["methodology"])