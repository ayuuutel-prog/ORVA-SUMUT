import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="ORVA SUMUT | Portal Informasi Padi",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# TEMA ORVA SUMUT: HIJAU + JINGGA
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --green: #174A32;
    --green2: #286B45;
    --orange: #F39A24;
    --orange2: #E98213;
    --cream: #FFF9EF;
    --ink: #24372D;
    --muted: #718078;
}
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp {
    background: linear-gradient(180deg, #FFF9EF 0%, #F7F8F1 55%, #FFF9EF 100%);
    color: var(--ink);
}
.block-container { padding-top: 1.25rem; padding-bottom: 2.5rem; max-width: 1500px; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F6A52E 0%, #F18D1D 58%, #E97B13 100%);
    border-right: 3px solid rgba(255,255,255,.35);
}
[data-testid="stSidebar"] * { color: #fff !important; }
[data-testid="stSidebar"] [data-testid="stForm"] {
    background: rgba(111,57,7,.13); padding: 13px;
    border: 1px solid rgba(255,255,255,.28); border-radius: 15px;
}
[data-testid="stSidebar"] .stButton button {
    background: #174A32 !important; color: #fff !important;
    border: 1px solid rgba(255,255,255,.25) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(255,255,255,.13); border-radius: 10px;
    padding: 5px 9px; margin-bottom: 3px;
}
.hero {
    position: relative; overflow: hidden; padding: 32px 34px;
    border-radius: 24px; margin-bottom: 22px; color: white;
    background:
      radial-gradient(circle at 86% 20%, rgba(255,190,75,.35), transparent 25%),
      linear-gradient(115deg, #123C2B 0%, #1B563C 60%, #39865A 100%);
    border: 1px solid rgba(243,154,36,.6);
    box-shadow: 0 15px 34px rgba(28,70,43,.15);
    animation: fadeUp .65s ease both;
}
.hero:after {
    content: "🌾"; position: absolute; right: 5%; bottom: -38px;
    font-size: 145px; opacity: .16; animation: bob 4s ease-in-out infinite;
}
.hero-kicker { color: #FFD58D; font-size: .72rem; font-weight: 800; letter-spacing: .17em; text-transform: uppercase; }
.hero-title {
    font-family: 'Times New Roman', Georgia, serif !important;
    font-size: clamp(2.3rem, 5vw, 3.7rem); font-weight: 700;
    line-height: 1.05; margin: 7px 0; color: #fff;
}
.hero-subtitle { color: #E9F2E9; font-size: .98rem; line-height: 1.7; max-width: 760px; }
.hero-tag {
    display: inline-block; margin-top: 15px; padding: 7px 13px;
    border-radius: 999px; border: 1px solid rgba(255,213,141,.6);
    background: rgba(255,255,255,.09); color: #FFE2B3; font-size: .72rem;
}
.section-kicker { color: #C27619; font-size: .69rem; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; margin-bottom: 3px; }
.section-title {
    color: #174A32; font-family: 'Times New Roman', Georgia, serif !important;
    font-size: 1.8rem; font-weight: 700; margin: 0 0 13px 0;
}
.metric-card {
    position: relative; overflow: hidden; min-height: 130px; padding: 17px;
    border-radius: 17px; border: 1px solid #E8E3D5;
    background: linear-gradient(145deg,#fff 0%,#F5F8EF 100%);
    box-shadow: 0 6px 18px rgba(30,65,42,.06);
    transition: transform .25s ease, box-shadow .25s ease;
    animation: fadeUp .6s ease both;
}
.metric-card:before { content:""; position:absolute; top:0; left:0; width:100%; height:4px; background:linear-gradient(90deg,#286B45,#F39A24); }
.metric-card:hover { transform: translateY(-5px); box-shadow: 0 13px 25px rgba(30,65,42,.12); }
.metric-icon { font-size: 1.45rem; margin-bottom: 6px; }
.metric-label { color:#718078; font-size:.73rem; font-weight:700; }
.metric-value { color:#174A32; font-size:clamp(1.1rem,1.8vw,1.65rem); font-weight:800; line-height:1.3; }
.metric-note { color:#89948C; font-size:.67rem; margin-top:3px; }
.info-card {
    background:#fff; border:1px solid #EAE4D7; border-radius:17px;
    padding:18px; box-shadow:0 5px 17px rgba(30,65,42,.045);
    height:100%;
}
.info-card h3 { color:#174A32; font-family:'Times New Roman',Georgia,serif; margin-top:0; }
.mascot-wrap { display:flex; align-items:center; gap:15px; }
.mascot {
    width:105px; min-width:105px; animation:bob 3s ease-in-out infinite;
    filter: drop-shadow(0 7px 5px rgba(0,0,0,.12));
}
.mascot-small { width:72px; min-width:72px; }
.mascot-note {
    background:#FFF0D7; border:1px solid #F5D29B; color:#714710;
    border-radius:16px; padding:12px 15px; line-height:1.55;
}
.stButton button, .stFormSubmitButton button, .stDownloadButton button {
    border-radius:11px; font-weight:700; transition:all .22s ease;
}
.stButton button:hover, .stFormSubmitButton button:hover, .stDownloadButton button:hover {
    transform:translateY(-2px); box-shadow:0 6px 15px rgba(23,74,50,.13);
}
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] {
    background:#1B563C; border-color:#1B563C;
}
[data-testid="stDataFrame"] { border:1px solid #E6E2D7; border-radius:12px; overflow:hidden; }
div[data-testid="stAlert"] { border-radius:13px; }
hr { border-color:#E9E3D7; }
.footer { text-align:center; color:#78857C; font-size:.75rem; padding:20px 0 4px; line-height:1.8; }
@keyframes fadeUp { from {opacity:0; transform:translateY(12px);} to {opacity:1; transform:translateY(0);} }
@keyframes bob { 0%,100% {transform:translateY(0);} 50% {transform:translateY(-8px);} }
@media(max-width:700px) {
    .hero { padding:24px 20px; }
    .hero:after { font-size:90px; right:2%; }
    .section-title { font-size:1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MASKOT ORVA (SVG BUATAN SENDIRI, TIDAK MEMERLUKAN FILE GAMBAR)
# =========================================================
def tampilkan_maskot(ukuran="normal"):
    kelas = "mascot mascot-small" if ukuran == "kecil" else "mascot"
    st.markdown(f"""
    <svg class="{kelas}" viewBox="0 0 180 190" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Maskot ORVA">
      <ellipse cx="91" cy="176" rx="48" ry="8" fill="#23452E" opacity=".13"/>
      <path d="M58 70 Q27 45 40 17 Q66 28 75 58 Q81 28 104 8 Q120 42 98 70" fill="#3F9B50" stroke="#1D6338" stroke-width="4"/>
      <path d="M73 69 Q91 24 135 25 Q129 58 99 77" fill="#69B94E" stroke="#1D6338" stroke-width="4"/>
      <g fill="#F6B72E" stroke="#C77B12" stroke-width="3">
        <ellipse cx="72" cy="38" rx="11" ry="20" transform="rotate(-35 72 38)"/>
        <ellipse cx="91" cy="24" rx="11" ry="21" transform="rotate(-12 91 24)"/>
        <ellipse cx="111" cy="29" rx="11" ry="20" transform="rotate(20 111 29)"/>
        <ellipse cx="128" cy="43" rx="10" ry="18" transform="rotate(43 128 43)"/>
        <ellipse cx="140" cy="60" rx="9" ry="16" transform="rotate(58 140 60)"/>
      </g>
      <path d="M51 79 Q51 54 88 49 Q128 50 132 83 L126 139 Q119 158 89 158 Q58 156 52 137Z" fill="#FFD45A" stroke="#C77B12" stroke-width="4"/>
      <ellipse cx="75" cy="101" rx="7" ry="10" fill="#2D3028"/>
      <ellipse cx="108" cy="101" rx="7" ry="10" fill="#2D3028"/>
      <circle cx="77" cy="98" r="2.5" fill="white"/><circle cx="110" cy="98" r="2.5" fill="white"/>
      <ellipse cx="63" cy="116" rx="9" ry="5" fill="#F28A75" opacity=".7"/>
      <ellipse cx="119" cy="116" rx="9" ry="5" fill="#F28A75" opacity=".7"/>
      <path d="M82 119 Q92 132 103 119" fill="none" stroke="#713B20" stroke-width="4" stroke-linecap="round"/>
      <path d="M61 143 Q90 155 122 143 L119 171 Q91 181 64 170Z" fill="#1E6840" stroke="#16492F" stroke-width="3"/>
      <path d="M70 153 Q91 162 111 153" fill="none" stroke="#F6B72E" stroke-width="4"/>
      <path d="M59 153 Q37 145 31 126" fill="none" stroke="#FFD45A" stroke-width="9" stroke-linecap="round"/>
      <circle cx="29" cy="123" r="9" fill="#FFD45A" stroke="#C77B12" stroke-width="3"/>
      <path d="M125 153 Q148 146 151 128" fill="none" stroke="#FFD45A" stroke-width="9" stroke-linecap="round"/>
      <circle cx="152" cy="125" r="9" fill="#FFD45A" stroke="#C77B12" stroke-width="3"/>
      <path d="M76 172 L72 183 M108 172 L112 183" stroke="#16492F" stroke-width="7" stroke-linecap="round"/>
      <path d="M62 184 Q74 177 84 184 L83 190 L61 190Z M101 184 Q113 177 124 184 L126 190 L103 190Z" fill="#F8F4E8" stroke="#16492F" stroke-width="3"/>
    </svg>
    """, unsafe_allow_html=True)

# =========================================================
# LOGIN ADMIN
# =========================================================
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# =========================================================
# SIDEBAR DAN NAVIGASI
# =========================================================
menu_halaman = [
    "🏠 Beranda",
    "📊 Data & Statistik",
    "🌾 Mengenal Padi",
    "🌱 Varietas Padi",
    "🧑‍🌾 Panduan Budidaya",
    "🗓️ Kalender Tanam",
    "💡 Wawasan Pertanian",
    "📚 Sumber Data",
    "ℹ️ Tentang ORVA"
]

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:8px 0 3px;">
      <div style="font-size:2.6rem;">🌾</div>
      <div style="font-family:'Times New Roman',serif;font-size:2rem;font-weight:bold;line-height:1;color:#fff;">ORVA<br>SUMUT</div>
      <div style="font-size:.68rem;letter-spacing:.09em;margin-top:8px;">PORTAL INFORMASI PADI</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("### 🧭 Navigasi")
    halaman = st.radio("Pilih halaman", menu_halaman, label_visibility="collapsed")
    st.divider()
    st.markdown("### 👤 Akses Pengguna")
    if not st.session_state.admin_logged_in:
        st.info("Mode Pengunjung")
        with st.form("login_admin"):
            password = st.text_input("Password Admin", type="password")
            login_button = st.form_submit_button("Masuk sebagai Admin", use_container_width=True)
        if login_button:
            if password == st.secrets["ADMIN_PASSWORD"]:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Password tidak sesuai.")
    else:
        st.success("Login sebagai Admin")
        if st.button("Logout", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()
    st.divider()
    st.caption("Hak akses: " + ("Admin" if st.session_state.admin_logged_in else "Pengunjung"))
    st.caption("Oriza Sativa Sumatera Utara")

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
  <div class="hero-kicker">Integrated Rice Data & Knowledge Portal · Sumatera Utara</div>
  <h1 class="hero-title">ORVA SUMUT</h1>
  <div class="hero-subtitle">Oriza Sativa Sumatera Utara — portal informasi produksi, pengetahuan, dan perkembangan pertanian padi di Sumatera Utara.</div>
  <div class="hero-tag">🌱 DATA TERINTEGRASI · EDUKASI PERTANIAN · SUMATERA UTARA</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# HALAMAN BERANDA
# =========================================================
if halaman == "🏠 Beranda":
    col_welcome, col_mascot = st.columns([3.4, 1])
    with col_welcome:
        st.markdown('<div class="section-kicker">Selamat datang</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Satu Portal untuk Mengenal Produksi Padi Sumatera Utara</div>', unsafe_allow_html=True)
        st.write("ORVA SUMUT menggabungkan data produksi padi dari beberapa kabupaten dengan informasi edukatif seputar tanaman padi. Pengunjung dapat melihat statistik, mempelajari varietas, dan membaca panduan pertanian.")
        st.markdown('<div class="mascot-note">🌾 <b>Halo, Sahabat ORVA!</b><br>Yuk, jelajahi data dan pengetahuan padi Sumatera Utara. Semoga informasi di sini bermanfaat!</div>', unsafe_allow_html=True)
    with col_mascot:
        tampilkan_maskot()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">Jelajahi ORVA</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Apa yang ingin kamu ketahui?</div>', unsafe_allow_html=True)
    cards = st.columns(3)
    info_cards = [
        ("📊", "Data & Statistik", "Lihat produksi, luas panen, produktivitas, grafik, dan sebaran kabupaten."),
        ("🌾", "Mengenal Padi", "Kenali jenis tanaman padi, bagian tanaman, dan fase pertumbuhannya."),
        ("🌱", "Varietas Padi", "Pelajari contoh varietas dan karakteristik yang perlu diperhatikan."),
        ("🧑‍🌾", "Panduan Budidaya", "Baca ringkasan tahapan budidaya padi dari persiapan hingga panen."),
        ("🗓️", "Kalender Tanam", "Kenali faktor yang perlu diperiksa sebelum menentukan waktu tanam."),
        ("💡", "Wawasan Pertanian", "Pahami indikator produksi dan informasi pascapanen.")
    ]
    for i, item in enumerate(info_cards):
        with cards[i % 3]:
            st.markdown(f'<div class="info-card"><div style="font-size:1.8rem">{item[0]}</div><h3>{item[1]}</h3><p>{item[2]}</p></div>', unsafe_allow_html=True)
    st.caption("Gunakan menu navigasi di sebelah kiri untuk membuka setiap bagian.")

# =========================================================
# HALAMAN DATA & STATISTIK
# =========================================================
elif halaman == "📊 Data & Statistik":
    st.markdown('<div class="section-kicker">Dashboard data</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Produksi Padi Kabupaten Terintegrasi</div>', unsafe_allow_html=True)
    try:
        with psycopg2.connect(st.secrets["DB_PUSAT"]) as conn:
            df = pd.read_sql_query("""
                SELECT id_produksi, nama_kabupaten_kota, tahun, luas_panen,
                       produktivitas, jumlah_produksi, updated_at
                FROM produksi_padi
                ORDER BY nama_kabupaten_kota, tahun
            """, conn)

        for kolom in ["luas_panen", "produktivitas", "jumlah_produksi"]:
            df[kolom] = pd.to_numeric(df[kolom], errors="coerce").fillna(0)
        df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce")

        if df.empty:
            st.warning("Database pusat belum memiliki data produksi padi.")
        else:
            total_kabupaten = df["nama_kabupaten_kota"].nunique()
            total_data = len(df)
            total_produksi = df["jumlah_produksi"].sum()
            total_luas = df["luas_panen"].sum()
            rata_produktivitas = df["produktivitas"].mean()
            metrics = [
                ("🗺️", "Kabupaten Terintegrasi", f"{total_kabupaten}", "Wilayah dalam sistem"),
                ("🗃️", "Total Data", f"{total_data:,}", "Catatan produksi tersimpan"),
                ("🌾", "Total Produksi", f"{total_produksi:,.2f} ton", "Akumulasi seluruh data"),
                ("📐", "Luas Panen", f"{total_luas:,.2f} ha", "Akumulasi luas panen"),
                ("📈", "Rata-rata Produktivitas", f"{rata_produktivitas:,.2f}", "kuintal per hektare")
            ]
            metric_cols = st.columns(5)
            for col, item in zip(metric_cols, metrics):
                with col:
                    st.markdown(f'<div class="metric-card"><div class="metric-icon">{item[0]}</div><div class="metric-label">{item[1]}</div><div class="metric-value">{item[2]}</div><div class="metric-note">{item[3]}</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-kicker">Eksplorasi data</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Filter Data Produksi</div>', unsafe_allow_html=True)
            with st.container(border=True):
                f1, f2 = st.columns(2)
                with f1:
                    kabupaten_list = sorted(df["nama_kabupaten_kota"].dropna().unique())
                    pilihan_kabupaten = st.multiselect("Pilih Kabupaten", kabupaten_list, default=kabupaten_list)
                with f2:
                    tahun_list = sorted(df["tahun"].dropna().astype(int).unique())
                    pilihan_tahun = st.multiselect("Pilih Tahun", tahun_list, default=tahun_list)
            data_filter = df[
                df["nama_kabupaten_kota"].isin(pilihan_kabupaten) &
                df["tahun"].isin(pilihan_tahun)
            ].copy()

            if data_filter.empty:
                st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
            else:
                st.markdown('<div class="section-kicker">Analisis komparatif</div>', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Perbandingan Produksi Antar Kabupaten</div>', unsafe_allow_html=True)
                data_grafik = data_filter.groupby("nama_kabupaten_kota", as_index=False)["jumlah_produksi"].sum().sort_values("jumlah_produksi")
                fig1 = px.bar(data_grafik, x="jumlah_produksi", y="nama_kabupaten_kota", orientation="h",
                              color="jumlah_produksi", color_continuous_scale=["#F8D9A8", "#EFA13A", "#1B563C"],
                              labels={"nama_kabupaten_kota":"Kabupaten", "jumlah_produksi":"Produksi (ton)"},
                              text="jumlah_produksi")
                fig1.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
                fig1.update_layout(height=380, margin=dict(l=10,r=65,t=20,b=35),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Plus Jakarta Sans, sans-serif",color="#294536"),
                    coloraxis_showscale=False, xaxis=dict(showgrid=True,gridcolor="#E8EEE7",title="Produksi (ton)"),
                    yaxis=dict(title="",showgrid=False), hoverlabel=dict(bgcolor="#174A32",font_color="white"))

                st.markdown('<div class="section-kicker">Tren tahunan</div>', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Perkembangan Produksi Padi</div>', unsafe_allow_html=True)
                data_tahun = data_filter.groupby("tahun", as_index=False)["jumlah_produksi"].sum().sort_values("tahun")
                fig2 = px.line(data_tahun, x="tahun", y="jumlah_produksi", markers=True,
                               labels={"tahun":"Tahun","jumlah_produksi":"Produksi (ton)"})
                fig2.update_traces(line=dict(color="#1B563C",width=4),
                    marker=dict(size=10,color="#F39A24",line=dict(width=2,color="#FFFFFF")))
                fig2.update_layout(height=340,margin=dict(l=10,r=20,t=20,b=35),
                    paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Plus Jakarta Sans, sans-serif",color="#294536"),
                    xaxis=dict(showgrid=False,title="Tahun",tickformat="d"),
                    yaxis=dict(showgrid=True,gridcolor="#E8EEE7",title="Produksi (ton)"),
                    hoverlabel=dict(bgcolor="#174A32",font_color="white"))
                c1,c2 = st.columns(2)
                with c1:
                    with st.container(border=True): st.plotly_chart(fig1,use_container_width=True)
                with c2:
                    with st.container(border=True): st.plotly_chart(fig2,use_container_width=True)

                st.markdown('<div class="section-kicker">Sebaran wilayah</div>', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Peta Kabupaten Terintegrasi</div>', unsafe_allow_html=True)
                koordinat = pd.DataFrame([
                    {"nama_kabupaten_kota":"Deli Serdang","lat":3.420,"lon":98.704},
                    {"nama_kabupaten_kota":"Serdang Bedagai","lat":3.390,"lon":99.020},
                    {"nama_kabupaten_kota":"Simalungun","lat":2.960,"lon":99.060},
                    {"nama_kabupaten_kota":"Tapanuli Utara","lat":2.000,"lon":99.070},
                    {"nama_kabupaten_kota":"Langkat","lat":3.850,"lon":98.300}
                ])
                peta_data = koordinat[koordinat["nama_kabupaten_kota"].isin(pilihan_kabupaten)]
                if not peta_data.empty:
                    fig_map = px.scatter_geo(peta_data,lat="lat",lon="lon",text="nama_kabupaten_kota",
                                             hover_name="nama_kabupaten_kota",projection="mercator")
                    fig_map.update_traces(marker=dict(size=13,color="#F39A24",line=dict(width=2,color="#174A32")),
                                          textposition="top center",textfont=dict(size=11,color="#173D2C"))
                    fig_map.update_geos(scope="asia",center=dict(lat=2.5,lon=98.8),
                        lataxis_range=[-1,7],lonaxis_range=[94,102],showcountries=True,
                        countrycolor="#B8C9BA",showland=True,landcolor="#EEF3EA",
                        showocean=True,oceancolor="#E7F0F2",showcoastlines=True,
                        coastlinecolor="#A8BDAE",showframe=False,bgcolor="rgba(0,0,0,0)")
                    with st.container(border=True):
                        st.caption("Titik menunjukkan lokasi perkiraan kabupaten, bukan batas administrasi resmi.")
                        st.plotly_chart(fig_map,use_container_width=True)

                st.markdown('<div class="section-kicker">Data terperinci</div>', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Tabel Produksi Padi</div>', unsafe_allow_html=True)
                kolom_tampil = ["nama_kabupaten_kota","tahun","luas_panen","produktivitas","jumlah_produksi","updated_at"]
                nama_kolom = {"nama_kabupaten_kota":"Kabupaten/Kota","tahun":"Tahun",
                    "luas_panen":"Luas Panen (ha)","produktivitas":"Produktivitas (ku/ha)",
                    "jumlah_produksi":"Produksi (ton)","updated_at":"Terakhir Diperbarui"}
                tabel_tampil = data_filter[kolom_tampil].rename(columns=nama_kolom)
                with st.container(border=True):
                    st.dataframe(tabel_tampil,use_container_width=True,hide_index=True,
                        column_config={
                            "Luas Panen (ha)":st.column_config.NumberColumn(format="%.2f"),
                            "Produktivitas (ku/ha)":st.column_config.NumberColumn(format="%.2f"),
                            "Produksi (ton)":st.column_config.NumberColumn(format="%.2f"),
                            "Terakhir Diperbarui":st.column_config.DatetimeColumn(format="DD MMM YYYY, HH:mm")
                        })
                    st.download_button("⬇️ Unduh Data Terfilter (CSV)",
                        data=tabel_tampil.to_csv(index=False).encode("utf-8-sig"),
                        file_name="data_produksi_padi_orva_sumut.csv",mime="text/csv")
            st.caption(f"Data terakhir diperbarui: {df['updated_at'].max()}")

    except Exception as e:
        st.error("Terjadi kesalahan saat mengambil data dari database pusat.")
        st.caption(str(e))

    # -----------------------------------------------------
    # PENGELOLAAN DATA ADMIN (FITUR LAMA DIPERTAHANKAN)
    # -----------------------------------------------------
    if st.session_state.admin_logged_in:
        st.divider()
        st.markdown('<div class="section-kicker">Panel administrator</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Pengelolaan Data Produksi Padi</div>', unsafe_allow_html=True)
        menu_admin = st.selectbox("Pilih Pengelolaan Data",["Tambah Data","Edit Data","Hapus Data"])
        daftar_database = {
            "Deli Serdang":"DB_DELI_SERDANG",
            "Serdang Bedagai":"DB_SERDANG_BEDAGAI",
            "Simalungun":"DB_SIMALUNGUN",
            "Tapanuli Utara":"DB_TAPANULI_UTARA",
            "Langkat":"DB_LANGKAT"
        }

        if menu_admin == "Tambah Data":
            st.subheader("➕ Tambah Data Produksi Padi")
            with st.form("form_tambah_data"):
                kabupaten = st.selectbox("Kabupaten",list(daftar_database.keys()))
                tahun = st.number_input("Tahun",min_value=2000,max_value=2100,value=2025,step=1)
                luas_panen = st.number_input("Luas Panen (ha)",min_value=0.0,step=0.01)
                produktivitas = st.number_input("Produktivitas (ku/ha)",min_value=0.0,step=0.01)
                jumlah_produksi = st.number_input("Jumlah Produksi (ton)",min_value=0.0,step=0.01)
                simpan = st.form_submit_button("Simpan Data",use_container_width=True)
            if simpan:
                try:
                    with psycopg2.connect(st.secrets[daftar_database[kabupaten]]) as conn:
                        with conn.cursor() as cursor:
                            cursor.execute("""INSERT INTO produksi_padi
                                (nama_kabupaten_kota,tahun,luas_panen,produktivitas,jumlah_produksi)
                                VALUES (%s,%s,%s,%s,%s)""",
                                (kabupaten,int(tahun),luas_panen,produktivitas,jumlah_produksi))
                    st.success("Data berhasil disimpan!")
                    st.rerun()
                except psycopg2.errors.UniqueViolation:
                    st.error("Data kabupaten dan tahun tersebut sudah tersedia.")
                except Exception as e:
                    st.error("Gagal menyimpan data.")
                    st.caption(str(e))

        elif menu_admin == "Edit Data":
            st.subheader("✏️ Edit Data Produksi Padi")
            kabupaten_edit = st.selectbox("Pilih Kabupaten",list(daftar_database.keys()),key="kabupaten_edit")
            try:
                with psycopg2.connect(st.secrets[daftar_database[kabupaten_edit]]) as conn:
                    data_edit = pd.read_sql_query("""SELECT id_produksi,tahun,luas_panen,produktivitas,jumlah_produksi
                        FROM produksi_padi ORDER BY tahun""",conn)
                if data_edit.empty:
                    st.warning("Belum ada data untuk kabupaten ini.")
                else:
                    st.dataframe(data_edit,use_container_width=True,hide_index=True)
                    id_edit = st.selectbox("Pilih ID Data yang akan diedit",data_edit["id_produksi"].tolist(),key="id_edit")
                    baris = data_edit[data_edit["id_produksi"]==id_edit].iloc[0]
                    with st.form("form_edit_data"):
                        tahun_baru = st.number_input("Tahun",min_value=2000,max_value=2100,value=int(baris["tahun"]),step=1)
                        luas_baru = st.number_input("Luas Panen (ha)",min_value=0.0,value=float(baris["luas_panen"]),step=0.01)
                        produktivitas_baru = st.number_input("Produktivitas (ku/ha)",min_value=0.0,value=float(baris["produktivitas"]),step=0.01)
                        produksi_baru = st.number_input("Jumlah Produksi (ton)",min_value=0.0,value=float(baris["jumlah_produksi"]),step=0.01)
                        tombol_edit = st.form_submit_button("Simpan Perubahan",use_container_width=True)
                    if tombol_edit:
                        with psycopg2.connect(st.secrets[daftar_database[kabupaten_edit]]) as conn:
                            with conn.cursor() as cursor:
                                cursor.execute("""UPDATE produksi_padi SET tahun=%s,luas_panen=%s,
                                    produktivitas=%s,jumlah_produksi=%s,updated_at=NOW()
                                    WHERE id_produksi=%s""",
                                    (int(tahun_baru),luas_baru,produktivitas_baru,produksi_baru,int(id_edit)))
                        st.success("Data berhasil diperbarui!")
                        st.rerun()
            except Exception as e:
                st.error("Gagal mengedit data.")
                st.caption(str(e))

        elif menu_admin == "Hapus Data":
            st.subheader("🗑️ Hapus Data Produksi Padi")
            kabupaten_hapus = st.selectbox("Pilih Kabupaten",list(daftar_database.keys()),key="kabupaten_hapus")
            try:
                with psycopg2.connect(st.secrets[daftar_database[kabupaten_hapus]]) as conn:
                    data_hapus = pd.read_sql_query("""SELECT id_produksi,tahun,luas_panen,produktivitas,jumlah_produksi
                        FROM produksi_padi ORDER BY tahun""",conn)
                if data_hapus.empty:
                    st.warning("Belum ada data untuk kabupaten ini.")
                else:
                    st.dataframe(data_hapus,use_container_width=True,hide_index=True)
                    id_hapus = st.selectbox("Pilih ID Data yang akan dihapus",data_hapus["id_produksi"].tolist(),key="id_hapus")
                    konfirmasi = st.checkbox("Saya yakin ingin menghapus data ini.")
                    if st.button("Hapus Data",use_container_width=True,disabled=not konfirmasi):
                        with psycopg2.connect(st.secrets[daftar_database[kabupaten_hapus]]) as conn:
                            with conn.cursor() as cursor:
                                cursor.execute("DELETE FROM produksi_padi WHERE id_produksi=%s",(int(id_hapus),))
                        st.success("Data berhasil dihapus!")
                        st.rerun()
            except Exception as e:
                st.error("Gagal menghapus data.")
                st.caption(str(e))
    else:
        st.info("Login sebagai Admin untuk mengakses pengelolaan data.")

# =========================================================
# HALAMAN MENGENAL PADI
# =========================================================
elif halaman == "🌾 Mengenal Padi":
    st.markdown('<div class="section-kicker">Ensiklopedia padi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Mengenal Tanaman Padi</div>', unsafe_allow_html=True)
    a,b = st.columns([3,1])
    with a:
        st.write("Padi (*Oryza sativa* L.) merupakan tanaman pangan yang menghasilkan gabah. Setelah melalui proses penggilingan, gabah menjadi beras yang menjadi salah satu sumber pangan utama masyarakat Indonesia.")
        st.write("Pertumbuhan tanaman padi dipengaruhi oleh varietas, kondisi tanah, ketersediaan air, iklim, pengelolaan hara, serta pengendalian organisme pengganggu tanaman.")
    with b:
        tampilkan_maskot("kecil")
    st.markdown("### Jenis lingkungan budidaya padi")
    jenis = st.columns(3)
    with jenis[0]:
        st.markdown('<div class="info-card"><h3>🌊 Padi Sawah</h3><p>Dibudidayakan pada lahan yang umumnya memiliki pengelolaan air atau genangan, baik melalui irigasi maupun tadah hujan.</p></div>',unsafe_allow_html=True)
    with jenis[1]:
        st.markdown('<div class="info-card"><h3>⛰️ Padi Gogo</h3><p>Dibudidayakan di lahan kering dan mengandalkan curah hujan serta pengelolaan kelembapan tanah.</p></div>',unsafe_allow_html=True)
    with jenis[2]:
        st.markdown('<div class="info-card"><h3>🌿 Padi Rawa</h3><p>Dibudidayakan pada lahan rawa dengan kondisi tata air yang khas dan perlu dikelola sesuai karakter lahannya.</p></div>',unsafe_allow_html=True)
    st.markdown("### Tahapan pertumbuhan padi")
    tahapan = [
        ("01","Perkecambahan","Benih mulai berkecambah dan membentuk akar serta tunas."),
        ("02","Bibit dan anakan","Tanaman membentuk daun dan anakan."),
        ("03","Pemanjangan batang","Batang tumbuh dan tanaman memasuki fase reproduktif."),
        ("04","Pembungaan","Malai keluar dan bunga padi mengalami penyerbukan."),
        ("05","Pengisian gabah","Bulir berkembang dan mengisi hingga matang."),
        ("06","Panen","Padi dipanen ketika telah mencapai kematangan yang sesuai.")
    ]
    cols = st.columns(3)
    for i,(nomor,nama,uraian) in enumerate(tahapan):
        with cols[i%3]:
            st.markdown(f'<div class="info-card"><div style="color:#E98213;font-weight:800;font-size:1.2rem">{nomor}</div><h3>{nama}</h3><p>{uraian}</p></div>',unsafe_allow_html=True)

# =========================================================
# HALAMAN VARIETAS PADI
# =========================================================
elif halaman == "🌱 Varietas Padi":
    st.markdown('<div class="section-kicker">Pengetahuan varietas</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Mengenal Varietas Padi</div>', unsafe_allow_html=True)
    st.info("Informasi berikut merupakan pengenalan umum. Kesesuaian varietas dan potensi hasil harus diperiksa melalui deskripsi resmi varietas serta rekomendasi setempat.")
    varietas = [
        ("Ciherang","Salah satu varietas padi sawah yang banyak dikenal petani. Pemilihan benih tetap perlu mempertimbangkan kondisi lahan dan rekomendasi wilayah."),
        ("Mekongga","Varietas padi sawah yang dikenal luas. Perhatikan kesesuaian agroekosistem dan ketahanan terhadap organisme pengganggu."),
        ("Inpari 32","Termasuk kelompok Inpari (Inbrida Padi Irigasi). Informasi resmi mengenai karakter dan ketahanannya perlu merujuk deskripsi varietas."),
        ("Inpari 42","Salah satu varietas Inpari yang dapat dipelajari karakteristiknya melalui katalog resmi varietas tanaman pangan.")
    ]
    cols = st.columns(2)
    for i,(nama,deskripsi) in enumerate(varietas):
        with cols[i%2]:
            st.markdown(f'<div class="info-card"><div style="font-size:1.5rem">🌾</div><h3>{nama}</h3><p>{deskripsi}</p></div>',unsafe_allow_html=True)
    st.markdown("### Hal yang perlu diperhatikan saat memilih varietas")
    st.markdown("""
    - **Kesesuaian lahan:** perhatikan jenis lahan, ketersediaan air, dan kondisi tanah.
    - **Umur tanaman:** sesuaikan dengan kalender tanam dan ketersediaan air.
    - **Ketahanan:** cek informasi ketahanan terhadap hama dan penyakit yang umum di wilayah setempat.
    - **Mutu benih:** gunakan benih bermutu dan sumber yang dapat dipercaya.
    - **Rekomendasi lokal:** konsultasikan pilihan varietas dengan penyuluh pertanian atau instansi terkait.
    """)

# =========================================================
# HALAMAN PANDUAN BUDIDAYA
# =========================================================
elif halaman == "🧑‍🌾 Panduan Budidaya":
    st.markdown('<div class="section-kicker">Panduan praktis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Tahapan Umum Budidaya Padi</div>', unsafe_allow_html=True)
    st.warning("Panduan ini bersifat edukatif dan umum. Praktik di lapangan perlu disesuaikan dengan varietas, kondisi lahan, musim, dan arahan penyuluh setempat.")
    langkah = [
        ("Persiapan lahan","Periksa kondisi tanah, sumber air, drainase, dan riwayat lahan. Siapkan lahan sesuai sistem budidaya yang digunakan."),
        ("Pemilihan benih","Pilih benih bermutu, berlabel, dan sesuai dengan kondisi agroekosistem setempat."),
        ("Persemaian dan tanam","Atur persemaian atau penanaman langsung sesuai rekomendasi varietas dan sistem tanam."),
        ("Pengelolaan air","Jaga ketersediaan air dan drainase. Kebutuhan air dapat berbeda menurut fase pertumbuhan dan kondisi lahan."),
        ("Pemupukan","Lakukan pemupukan berdasarkan kebutuhan tanaman dan kondisi tanah, idealnya mengacu pada rekomendasi pemupukan setempat."),
        ("Pengendalian OPT","Lakukan pengamatan rutin. Terapkan pengendalian hama dan penyakit secara terpadu serta utamakan tindakan yang tepat sasaran."),
        ("Panen dan pascapanen","Panen pada tingkat kematangan yang sesuai, kemudian lakukan perontokan, pengeringan, dan penyimpanan secara baik.")
    ]
    for i,(judul,uraian) in enumerate(langkah,1):
        with st.expander(f"{i}. {judul}",expanded=(i==1)):
            st.write(uraian)
    st.markdown('<div class="mascot-note">🌱 <b>Pesan ORVA:</b> budidaya yang baik dimulai dari pengamatan kondisi lahan dan keputusan yang sesuai kebutuhan setempat.</div>',unsafe_allow_html=True)

# =========================================================
# HALAMAN KALENDER TANAM
# =========================================================
elif halaman == "🗓️ Kalender Tanam":
    st.markdown('<div class="section-kicker">Perencanaan musim</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Informasi Kalender Tanam</div>', unsafe_allow_html=True)
    st.write("Waktu tanam padi tidak dapat disamaratakan untuk seluruh Sumatera Utara. Penentuan jadwal perlu mempertimbangkan curah hujan, ketersediaan irigasi, kondisi lahan, pola tanam, dan prakiraan iklim.")
    st.markdown("### Sebelum menentukan waktu tanam")
    checks = [
        "Periksa prakiraan musim dan informasi iklim terbaru dari BMKG.",
        "Pastikan ketersediaan air dan kondisi saluran irigasi.",
        "Perhatikan jadwal tanam kelompok tani dan kondisi lahan sekitar.",
        "Pilih varietas dengan umur dan karakter yang sesuai.",
        "Konsultasikan jadwal dengan penyuluh pertanian setempat."
    ]
    for item in checks:
        st.markdown(f"- {item}")
    st.warning("ORVA tidak menampilkan tanggal tanam otomatis karena rekomendasi tanam harus berbasis data iklim dan kondisi lokal terbaru. Hindari menggunakan kalender umum sebagai kepastian jadwal.")
    st.markdown("**Sumber informasi yang dapat diperiksa:** BMKG, Kementerian Pertanian, Dinas Pertanian setempat, dan penyuluh pertanian.")

# =========================================================
# HALAMAN WAWASAN PERTANIAN
# =========================================================
elif halaman == "💡 Wawasan Pertanian":
    st.markdown('<div class="section-kicker">Memahami angka pertanian</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Wawasan Produksi dan Pascapanen</div>', unsafe_allow_html=True)
    indikator = st.columns(3)
    with indikator[0]:
        st.markdown('<div class="info-card"><h3>📐 Luas Panen</h3><p>Luas tanaman yang dipanen pada periode tertentu. Angka ini berbeda dari luas lahan baku atau luas tanam.</p></div>',unsafe_allow_html=True)
    with indikator[1]:
        st.markdown('<div class="info-card"><h3>📈 Produktivitas</h3><p>Hasil produksi per satuan luas panen. Dalam data padi, satuan yang sering digunakan adalah kuintal per hektare (ku/ha).</p></div>',unsafe_allow_html=True)
    with indikator[2]:
        st.markdown('<div class="info-card"><h3>🌾 Produksi</h3><p>Total hasil panen pada wilayah dan periode tertentu. Produksi dipengaruhi luas panen dan produktivitas.</p></div>',unsafe_allow_html=True)
    st.markdown("### Mengapa produksi bisa berubah?")
    st.markdown("""
    - Perubahan luas panen dan luas tanam.
    - Perbedaan kondisi cuaca dan ketersediaan air.
    - Perubahan produktivitas akibat varietas dan pengelolaan budidaya.
    - Serangan hama dan penyakit tanaman.
    - Perbedaan waktu panen dan pencatatan data.
    """)
    st.markdown("### Penanganan pascapanen")
    st.write("Penanganan setelah panen berpengaruh terhadap mutu dan kehilangan hasil. Tahap yang perlu diperhatikan meliputi perontokan, pembersihan, pengeringan, penggilingan, dan penyimpanan gabah atau beras.")
    st.info("Saat membandingkan angka antarwilayah atau tahun, pastikan definisi, satuan, periode, dan sumber datanya sama.")

# =========================================================
# HALAMAN SUMBER DATA
# =========================================================
elif halaman == "📚 Sumber Data":
    st.markdown('<div class="section-kicker">Transparansi informasi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Sumber dan Pengelolaan Data</div>', unsafe_allow_html=True)
    st.write("Data statistik produksi pada dashboard ORVA SUMUT berasal dari basis data yang diintegrasikan dari kabupaten yang telah terhubung ke sistem. Setiap angka perlu dibaca bersama tahun, satuan, dan sumber rujukannya.")
    st.markdown("### Sumber rujukan yang disarankan")
    st.markdown("""
    - **Badan Pusat Statistik (BPS):** statistik luas panen, produktivitas, dan produksi padi.
    - **Kementerian Pertanian:** informasi teknis budidaya dan varietas tanaman pangan.
    - **Badan Meteorologi, Klimatologi, dan Geofisika (BMKG):** informasi iklim dan prakiraan musim.
    - **Dinas Pertanian dan penyuluh:** rekomendasi teknis sesuai kondisi wilayah.
    """)
    st.markdown("### Catatan pembacaan data")
    st.markdown("""
    1. Perhatikan tahun data yang sedang ditampilkan.
    2. Luas panen menggunakan hektare (ha).
    3. Produktivitas menggunakan kuintal per hektare (ku/ha).
    4. Produksi menggunakan ton.
    5. Data yang belum tersedia tidak boleh dianggap bernilai nol.
    """)
    st.warning("Sebelum publikasi, lengkapi setiap dataset dengan tautan atau dokumen sumber resmi, tanggal akses, dan keterangan metode pengumpulan. Halaman ini merupakan daftar rujukan, bukan klaim bahwa seluruh konten telah diverifikasi dari sumber tersebut.")

# =========================================================
# HALAMAN TENTANG ORVA
# =========================================================
elif halaman == "ℹ️ Tentang ORVA":
    st.markdown('<div class="section-kicker">Mengenal platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Tentang ORVA SUMUT</div>', unsafe_allow_html=True)
    c1,c2 = st.columns([3,1])
    with c1:
        st.write("ORVA merupakan singkatan dari *Oriza Sativa Sumatera Utara*, sebuah portal informasi yang dirancang untuk menyajikan data produksi padi secara terintegrasi sekaligus menyediakan informasi edukatif mengenai tanaman padi.")
        st.write("Platform ini dikembangkan untuk membantu pengunjung mengakses ringkasan data, membandingkan indikator produksi, dan memperoleh pengetahuan dasar pertanian dalam satu tempat.")
        st.markdown("### Tujuan ORVA")
        st.markdown("- Menyediakan akses informasi produksi padi yang lebih terpusat.")
        st.markdown("- Membantu pembacaan data luas panen, produktivitas, dan produksi.")
        st.markdown("- Menyediakan materi edukasi dasar tentang tanaman padi.")
        st.markdown("- Mendorong pemanfaatan data dalam memahami kondisi pertanian daerah.")
    with c2:
        tampilkan_maskot()
    st.markdown('<div class="mascot-note">🌾 <b>Data Pertanian Terintegrasi, Pengetahuan untuk Masa Depan.</b></div>',unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
  <b>ORVA SUMUT</b> · Oriza Sativa Sumatera Utara<br>
  Portal Informasi Produksi dan Pengetahuan Padi Sumatera Utara
</div>
""", unsafe_allow_html=True)
