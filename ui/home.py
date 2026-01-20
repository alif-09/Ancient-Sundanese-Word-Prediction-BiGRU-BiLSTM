# ui/home.py
import os
import streamlit as st
from i18n import TEXTS

# ===== Data (Disesuaikan dengan Word-Level) =====
RESEARCHER = {
    "name": "Alif Al Husaini",
    "program_id": "Mahasiswa S1 Teknik Informatika, Universitas Padjadjaran",
    "program_en": "Undergraduate Student of Computer Science, Universitas Padjadjaran",
    "focus_id": "Fokus penelitian pada pemulihan kata yang hilang (Word-Level Restoration) berbasis konteks.",
    "focus_en": "Research focus on word-level restoration based on contextual modeling.",
    "affiliation_id": "Universitas Padjadjaran (UNPAD)",
    "affiliation_en": "Universitas Padjadjaran (UNPAD)",
    "email": "alhusainialif@gmail.com",
}
SUPERVISORS = [
    "Dr. Drs. Setiawan Hadi, M.Sc., CS.",
    "Dr. Deni Setiana, S.Si., M.Cs."
]

# ===== CSS (Tetap) =====
STYLE = """
<style>
/* Tabs pill di tengah */
div[data-baseweb="tab-list"]{ justify-content:center !important; gap:12px; }
button[data-baseweb="tab"]{
  background:#2b2e34; border-radius:12px; padding:10px 18px;
  color:#e5e7eb; font-weight:700; letter-spacing:.2px;
}
button[data-baseweb="tab"][aria-selected="true"]{ background:#ef4444; color:#fff; }
button[data-baseweb="tab"] span{ gap:8px; }

/* Heading section */
.section-title{ font-size:1.25rem; font-weight:800; letter-spacing:.25px; margin:6px 0 12px; }

/* Kartu & divider */
.card{ background:#1f2227; border:1px solid rgba(255,255,255,.08); border-radius:16px; padding:12px; }
.hr{ height:1px; background:linear-gradient(90deg,transparent,#38404a,transparent); border:0; margin:18px 0; }

/* Tabel key–value (kanan) */
.kvtable{
  width:100%; border-collapse:separate; border-spacing:0;
  background:#1f2227; border:1px solid rgba(255,255,255,.08); border-radius:16px; overflow:hidden;
}
.kvtable th, .kvtable td{ padding:10px 14px; vertical-align:top; }
.kvtable th{ width:200px; color:#9ca3af; text-align:left; font-weight:700; background:#1c1f24; }
.kvtable tr:nth-child(even) td{ background:#1b1e23; }
.kvtable td{ color:#e5e7eb; }
.kvtable .para{ padding:14px 16px; line-height:1.6; }

/* Kartu pembimbing */
.sup-grid{ display:flex; gap:16px; flex-wrap:wrap; margin-top:12px; }
.sup-card{ background:#1f2227; border:1px solid rgba(255,255,255,.08); border-radius:16px; padding:12px; width:240px; text-align:center; }
.sup-name{ font-weight:700; margin-top:8px; }
</style>
"""

def _img(path: str):
    return path if os.path.exists(path) else None

def show_home(language: str):
    st.markdown(STYLE, unsafe_allow_html=True)
    t = TEXTS[language]

    # Judul
    st.title(t["home_title"])

    # Tabs
    labels_id = ["Beranda", "Tentang Penelitian", "Cara Kerja"]
    labels_en = ["Landing", "About Research", "How It Works"]
    L = labels_id if language == "Indonesia" else labels_en
    tab_landing, tab_about, tab_how = st.tabs([f"🏠 {L[0]}", f"👤 {L[1]}", f"⚙️ {L[2]}"])

    # ===== Tab 1: Landing
    with tab_landing:
        st.markdown(t["home_intro"])
        st.info(t["cta_try"])
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Contoh Input (Word-Level):**")
            # Contoh diubah ke kalimat naskah dengan rumpang kata utuh
            st.code("patih sang sombali janma [mask] dibwatkeun", language="text")
        with c2:
            st.markdown("**Keluaran Sistem:**")
            st.write("- Model memprediksi satu kata utuh untuk mengisi rumpang.")
            st.write("- Menampilkan 10 kandidat kata (Top-10) beserta nilai probabilitasnya.")

    # ===== Tab 2: Tentang Penelitian
    with tab_about:
        st.markdown("<div class='section-title'>Identitas Peneliti</div>", unsafe_allow_html=True)

        if language == "Indonesia":
            thesis_para = (
                "Penelitian ini merupakan bagian dari tugas akhir (skripsi) yang berjudul: "
                "<b>“RESTORASI TEKS SUNDA KUNO PADA NASKAH LONTAR MENGGUNAKAN BI-GRU DAN BI-LSTM”</b>. "
                "Fokus utama sistem adalah memulihkan <b>kata yang hilang</b> secara utuh pada naskah historis."
            )
        else:
            thesis_para = (
                "This research is part of a final undergraduate thesis titled: "
                "<b>“Restoration of Ancient Sundanese Manuscripts using Bi-GRU and Bi-LSTM”</b>, "
                "focusing on the reconstruction of <b>missing whole words</b> based on ancient transliterated corpora."
            )
        st.markdown(f"<div class='card kvtable para' style='margin-bottom:12px'>{thesis_para}</div>", unsafe_allow_html=True)

        col_left, col_right = st.columns([0.9, 2.1], gap="large")

        with col_left:
            img = _img("assets/profile.jpg")
            if img:
                st.image(img, width=240)
            st.markdown(
                f"<div style='text-align:center; font-weight:600; color:#cbd5e1; margin-top:6px'>{RESEARCHER['name']}</div>",
                unsafe_allow_html=True
            )

        with col_right:
            if language == "Indonesia":
                rows = [
                    ("Nama:", RESEARCHER["name"]),
                    ("Program Studi:", RESEARCHER["program_id"]),
                    ("Institusi:", RESEARCHER["affiliation_id"]),
                    ("Fokus Penelitian:", RESEARCHER["focus_id"]),
                    ("Pembimbing:", f"1) {SUPERVISORS[0]} · 2) {SUPERVISORS[1]}"),
                    ("Email:", RESEARCHER["email"]),
                ]
            else:
                rows = [
                    ("Name:", RESEARCHER["name"]),
                    ("Program:", RESEARCHER["program_en"]),
                    ("Affiliation:", RESEARCHER["affiliation_en"]),
                    ("Research Focus:", RESEARCHER["focus_en"]),
                    ("Supervisors:", f"1) {SUPERVISORS[0]} · 2) {SUPERVISORS[1]}"),
                    ("Email:", RESEARCHER["email"]),
                ]
            html = ["<table class='kvtable'>"]
            for k, v in rows:
                html.append(f"<tr><th>{k}</th><td>{v}</td></tr>")
            html.append("</table>")
            st.markdown("".join(html), unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Pembimbing</div>", unsafe_allow_html=True)
        st.markdown("<div class='sup-grid'>", unsafe_allow_html=True)
        st.markdown("<div class='sup-card'>", unsafe_allow_html=True)
        sup1 = _img("assets/supervisor_1.jpg")
        if sup1: st.image(sup1, width=200)
        st.markdown(f"<div class='sup-name'>{SUPERVISORS[0]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='sup-card'>", unsafe_allow_html=True)
        sup2 = _img("assets/supervisor_2.jpg")
        if sup2: st.image(sup2, width=200)
        st.markdown(f"<div class='sup-name'>{SUPERVISORS[1]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True) 

    # ===== Tab 3: Cara Kerja (Disesuaikan dengan Word-Level Bi-RNN)
    with tab_how:
        if language == "Indonesia":
            st.markdown("<div class='section-title'>🔍 Alur Proses Restorasi Kata</div>", unsafe_allow_html=True)
            steps = [
                "Normalisasi — Pembersihan teks dari karakter non-alfabet dan penyesuaian huruf kecil.",
                "Sliding Window — Sistem mengambil konteks kata di sisi kiri dan kanan dari token `[mask]`.",
                "Word Tokenization — Konteks kata dipetakan ke dalam indeks numerik berdasarkan kamus kata (*Word-Vocab*).",
                "Inferensi Bi-RNN — Model Bi-GRU atau Bi-LSTM memproses urutan konteks secara dua arah (bidirectional).",
                "Softmax Ranking — Probabilitas dihitung untuk seluruh kosakata kata unik guna menentukan 10 kandidat terbaik (Top-10).",
                "Hasil Restorasi — Kandidat kata ditampilkan dengan nilai CER (*Character Error Rate*) untuk melihat kemiripan karakter."
            ]
        else:
            st.markdown("<div class='section-title'>🔍 Word Restoration Workflow</div>", unsafe_allow_html=True)
            steps = [
                "Normalization — Cleaning non-alphabetic characters and lowercasing the text.",
                "Sliding Window — Extracting surrounding word contexts for the `[mask]` token.",
                "Word Tokenization — Mapping words to numerical indices using a custom Word-Vocabulary.",
                "Bi-RNN Inference — Processing sequences bidirectionally using Bi-GRU or Bi-LSTM architectures.",
                "Softmax Ranking — Calculating probabilities across the unique word vocabulary to surface Top-10 candidates.",
                "Restoration Result — Displaying candidates with associated CER values to measure string similarity."
            ]
        for s in steps:
            st.markdown(f"- {s}")