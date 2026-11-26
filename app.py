import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="ORVA SUMUT | Dashboard Produksi Padi",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# TEMA PREMIUM ORVA SUMUT
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --forest: #123C2B;
    --forest2: #1B563C;
    --leaf: #2E8054;
    --gold: #D7AD55;
    --cream: #F7F8F3;
    --ink: #1C3026;
    --muted: #718078;
}
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: linear-gradient(180deg, #F4F7F2 0%, #FAFBF8 55%, #F4F7F2 100%);
    color: var(--ink);
}
.block-container {
    padding-top: 1.6rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #123C2B 0%, #0D3022 100%);
    border-right: 1px solid rgba(215,173,85,.25);
}
[data-testid="stSidebar"] * {
    color: #F4F7F1 !important;
}
[data-testid="stSidebar"] .stButton button {
    background: #D7AD55 !important;
    color: #173B2B !important;
    border: none !important;
    font-weight: 700 !important;
}
[data-testid="stSidebar"] [data-testid="stForm"] {
    background: rgba(255,255,255,.07);
    padding: 14px;
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 14px;
}
.hero {
    position: relative;
    overflow: hidden;
    padding: 32px 36px;
    border-radius: 22px;
    background:
      radial-gradient(circle at 86% 20%, rgba(215,173,85,.28), transparent 24%),
      linear-gradient(115deg, #103A29 0%, #1B563C 58%, #2E8054 100%);
    border: 1px solid rgba(215,173,85,.55);
    box-shadow: 0 14px 35px rgba(18,60,43,.14);
    color: #fff;
    margin-bottom: 22px;
}
.hero:after {
    content: "🌾";
    position: absolute;
    right: 5%;
    bottom: -30px;
    font-size: 145px;
    opacity: .13;
    transform: rotate(-13deg);
}
.hero-kicker {
    color: #E8CA87;
    font-size: .76rem;
    font-weight: 800;
    letter-spacing: .19em;
    text-transform: uppercase;
    margin-bottom: 9px;
}
.hero-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2rem, 4vw, 3.15rem);
    line-height: 1.08;
    font-weight: 700;
    color: #fff;
    margin: 0;
}
.hero-subtitle {
    color: #E5EFE7;
    font-size: 1rem;
    margin-top: 9px;
    max-width: 680px;
}
.hero-tag {
    display: inline-block;
    margin-top: 19px;
    border: 1px solid rgba(232,202,135,.55);
    color: #F2D99E;
    border-radius: 999px;
    padding: 6px 13px;
    font-size: .75rem;
    letter-spacing: .04em;
    background: rgba(255,255,255,.07);
}
.section-kicker {
    color: #9A7838;
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .16em;
    text-transform: uppercase;
    margin-bottom: 2px;
}
.section-title {
    color: #173D2C;
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.55rem;
    font-weight: 700;
    margin: 0 0 12px 0;
}
.metric-card {
    background: linear-gradient(145deg, #FFFFFF 0%, #F5F8F3 100%);
    border: 1px solid #DFE8DE;
    border-radius: 17px;
    padding: 17px 18px 15px 18px;
    box-shadow: 0 6px 18px rgba(25,65,43,.055);
    min-height: 122px;
    transition: transform .2s ease, box-shadow .2s ease;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 22px rgba(25,65,43,.10);
}
.metric-icon {
    font-size: 1.35rem;
    margin-bottom: 7px;
}
.metric-label {
    color: #718078;
    font-size: .77rem;
    font-weight: 700;
    letter-spacing: .035em;
}
.metric-value {
    color: #153F2C;
    font-size: clamp(1.25rem, 2vw, 1.8rem);
    font-weight: 800;
    line-height: 1.25;
    margin-top: 3px;
}
.metric-note {
    color: #8A968E;
    font-size: .7rem;
    margin-top: 3px;
}
.panel {
    background: #FFFFFF;
    border: 1px solid #E1E9E0;
    border-radius: 17px;
    padding: 17px 19px;
    box-shadow: 0 6px 18px rgba(25,65,43,.045);
}
div[data-testid="stDataFrame"] {
    border: 1px solid #DFE8DE;
    border-radius: 12px;
    overflow: hidden;
}
.stButton button, .stFormSubmitButton button {
    border-radius: 10px;
    font-weight: 700;
}
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] {
    background: #1B563C;
    border-color: #1B563C;
}
.stMultiSelect [data-baseweb="tag"] {
    background: #E4EFE5;
}
hr {
    border-color: #E1E9E0;
}
div[data-testid="stAlert"] {
    border-radius: 12px;
}
.footer {
    text-align: center;
    color: #7B8980;
    font-size: .78rem;
    padding: 16px 0 4px 0;
}
@media (max-width: 700px) {
    .hero { padding: 25px 22px; }
    .hero:after { font-size: 95px; right: 2%; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGIN ADMIN
# =========================================================
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

with st.sidebar:
    st.markdown("## 🌾 ORVA SUMUT")
    st.caption("PORTAL DATA PRODUKSI PADI")
    st.divider()
    st.markdown("### 👤 Akses Pengguna")

    if not st.session_state.admin_logged_in:
        st.info("Mode Pengunjung")
        with st.form("login_admin"):
            password = st.text_input("Password Admin", type="password")
            login_button = st.form_submit_button(
                "Masuk sebagai Admin", use_container_width=True
            )
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
    st.caption(
        "Hak akses: " +
        ("Admin" if st.session_state.admin_logged_in else "Pengunjung")
    )
    st.caption("Oriza Sativa Sumatera Utara")

# =========================================================
# HEADER / HERO
# =========================================================
st.markdown("""
<div class="hero">
  <div class="hero-kicker">Integrated Rice Data Platform · Sumatera Utara</div>
  <h1 class="hero-title">ORVA SUMUT</h1>
  <div class="hero-subtitle">
    Oriza Sativa Sumatera Utara — Sistem Integrasi Database Produksi Padi
    untuk menyajikan informasi produksi padi kabupaten secara terpusat.
  </div>
  <div class="hero-tag">🌱 DATA TERINTEGRASI · INFORMASI PERTANIAN · SUMATERA UTARA</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# KONEKSI DATABASE PUSAT
# =========================================================
try:
    with psycopg2.connect(st.secrets["DB_PUSAT"]) as conn:
        df = pd.read_sql_query("""
            SELECT
                id_produksi,
                nama_kabupaten_kota,
                tahun,
                luas_panen,
                produktivitas,
                jumlah_produksi,
                updated_at
            FROM produksi_padi
            ORDER BY nama_kabupaten_kota, tahun
        """, conn)

    # Normalisasi tipe data untuk perhitungan dan tampilan
    for kolom in ["luas_panen", "produktivitas", "jumlah_produksi"]:
        df[kolom] = pd.to_numeric(df[kolom], errors="coerce").fillna(0)
    df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce")

    st.markdown('<div class="section-kicker">Ringkasan utama</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Dashboard Produksi Padi</div>', unsafe_allow_html=True)

    if df.empty:
        st.warning("Database pusat belum memiliki data produksi padi.")
        data_tersedia = False
    else:
        data_tersedia = True

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
            ("📈", "Rata-rata Produktivitas", f"{rata_produktivitas:,.2f}", "kuintal per hektare"),
        ]

        metric_cols = st.columns(5)
        for col, item in zip(metric_cols, metrics):
            icon, label, value, note = item
            with col:
                st.markdown(f"""
                <div class="metric-card">
                  <div class="metric-icon">{icon}</div>
                  <div class="metric-label">{label}</div>
                  <div class="metric-value">{value}</div>
                  <div class="metric-note">{note}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # FILTER DATA
    # =====================================================
    st.markdown('<div class="section-kicker">Eksplorasi data</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Filter Data Produksi</div>', unsafe_allow_html=True)

    if data_tersedia:
        filter_panel = st.container(border=True)
        with filter_panel:
            col1, col2, col3 = st.columns([1.4, 1, 0.7])
            with col1:
                pilihan_kabupaten = st.multiselect(
                    "Pilih Kabupaten",
                    sorted(df["nama_kabupaten_kota"].dropna().unique()),
                    default=sorted(df["nama_kabupaten_kota"].dropna().unique())
                )
            with col2:
                pilihan_tahun = st.multiselect(
                    "Pilih Tahun",
                    sorted(df["tahun"].dropna().astype(int).unique()),
                    default=sorted(df["tahun"].dropna().astype(int).unique())
                )
            with col3:
                st.markdown(" ")
                st.metric("Data terpilih", int(
                    df["nama_kabupaten_kota"].isin(pilihan_kabupaten)
                    .mul(df["tahun"].isin(pilihan_tahun)).sum()
                ))

        data_filter = df[
            df["nama_kabupaten_kota"].isin(pilihan_kabupaten)
            & df["tahun"].isin(pilihan_tahun)
        ].copy()

        if data_filter.empty:
            st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
        else:
            # =================================================
            # GRAFIK PRODUKSI
            # =================================================
            st.markdown('<div class="section-kicker">Analisis komparatif</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Perbandingan Produksi Antar Kabupaten</div>', unsafe_allow_html=True)

            data_grafik = (
                data_filter.groupby("nama_kabupaten_kota", as_index=False)
                ["jumlah_produksi"].sum()
                .sort_values("jumlah_produksi", ascending=True)
            )

            fig1 = px.bar(
                data_grafik,
                x="jumlah_produksi",
                y="nama_kabupaten_kota",
                orientation="h",
                color="jumlah_produksi",
                color_continuous_scale=["#C7DCCB", "#2E8054", "#123C2B"],
                labels={
                    "nama_kabupaten_kota": "Kabupaten",
                    "jumlah_produksi": "Produksi (ton)"
                },
                text="jumlah_produksi"
            )
            fig1.update_traces(
                texttemplate="%{text:,.0f}",
                textposition="outside",
                cliponaxis=False,
                marker_line_width=0
            )
            fig1.update_layout(
                height=390,
                margin=dict(l=10, r=65, t=20, b=35),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans, sans-serif", color="#294536"),
                coloraxis_showscale=False,
                xaxis=dict(showgrid=True, gridcolor="#E8EEE7", zeroline=False, title="Produksi (ton)"),
                yaxis=dict(title="", showgrid=False),
                hoverlabel=dict(bgcolor="#123C2B", font_color="white")
            )

            # =================================================
            # GRAFIK PERKEMBANGAN
            # =================================================
            st.markdown('<div class="section-kicker">Tren tahunan</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Perkembangan Produksi Padi</div>', unsafe_allow_html=True)

            data_tahun = (
                data_filter.groupby("tahun", as_index=False)
                ["jumlah_produksi"].sum()
                .sort_values("tahun")
            )
            fig2 = px.line(
                data_tahun,
                x="tahun",
                y="jumlah_produksi",
                markers=True,
                labels={
                    "tahun": "Tahun",
                    "jumlah_produksi": "Produksi (ton)"
                }
            )
            fig2.update_traces(
                line=dict(color="#1B563C", width=4),
                marker=dict(size=10, color="#D7AD55", line=dict(width=2, color="#FFFFFF"))
            )
            fig2.update_layout(
                height=340,
                margin=dict(l=10, r=20, t=20, b=35),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans, sans-serif", color="#294536"),
                xaxis=dict(showgrid=False, title="Tahun", tickformat="d"),
                yaxis=dict(showgrid=True, gridcolor="#E8EEE7", zeroline=False, title="Produksi (ton)"),
                hoverlabel=dict(bgcolor="#123C2B", font_color="white")
            )

            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                with st.container(border=True):
                    st.plotly_chart(fig1, use_container_width=True)
            with chart_col2:
                with st.container(border=True):
                    st.plotly_chart(fig2, use_container_width=True)

            # =================================================
            # PETA LOKASI KABUPATEN
            # =================================================
            st.markdown('<div class="section-kicker">Sebaran wilayah</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Peta Kabupaten Terintegrasi di Sumatera Utara</div>', unsafe_allow_html=True)

            koordinat = pd.DataFrame([
                {"nama_kabupaten_kota": "Deli Serdang", "lat": 3.420, "lon": 98.704},
                {"nama_kabupaten_kota": "Serdang Bedagai", "lat": 3.390, "lon": 99.020},
                {"nama_kabupaten_kota": "Simalungun", "lat": 2.960, "lon": 99.060},
                {"nama_kabupaten_kota": "Tapanuli Utara", "lat": 2.000, "lon": 99.070},
                {"nama_kabupaten_kota": "Langkat", "lat": 3.850, "lon": 98.300},
            ])
            peta_data = koordinat[
                koordinat["nama_kabupaten_kota"].isin(pilihan_kabupaten)
            ].copy()

            if not peta_data.empty:
                fig_map = px.scatter_geo(
                    peta_data,
                    lat="lat",
                    lon="lon",
                    text="nama_kabupaten_kota",
                    hover_name="nama_kabupaten_kota",
                    projection="mercator"
                )
                fig_map.update_traces(
                    marker=dict(size=13, color="#D7AD55", line=dict(width=2, color="#123C2B")),
                    textposition="top center",
                    textfont=dict(size=11, color="#173D2C")
                )
                fig_map.update_geos(
                    scope="asia",
                    center=dict(lat=2.5, lon=98.8),
                    lataxis_range=[-1, 7],
                    lonaxis_range=[94, 102],
                    showcountries=True,
                    countrycolor="#B8C9BA",
                    showland=True,
                    landcolor="#EEF3EA",
                    showocean=True,
                    oceancolor="#E7F0F2",
                    showcoastlines=True,
                    coastlinecolor="#A8BDAE",
                    showframe=False,
                    bgcolor="rgba(0,0,0,0)"
                )
                fig_map.update_layout(
                    height=430,
                    margin=dict(l=0, r=0, t=10, b=0),
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="DM Sans, sans-serif", color="#294536")
                )
                with st.container(border=True):
                    st.caption("Titik menunjukkan lokasi perkiraan kabupaten, bukan batas administrasi resmi.")
                    st.plotly_chart(fig_map, use_container_width=True)
            else:
                st.info("Pilih setidaknya satu kabupaten untuk menampilkan peta.")

            # =================================================
            # TABEL DATA
            # =================================================
            st.markdown('<div class="section-kicker">Data terperinci</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Data Produksi Padi</div>', unsafe_allow_html=True)

            kolom_tampil = [
                "nama_kabupaten_kota", "tahun", "luas_panen",
                "produktivitas", "jumlah_produksi", "updated_at"
            ]
            nama_kolom = {
                "nama_kabupaten_kota": "Kabupaten/Kota",
                "tahun": "Tahun",
                "luas_panen": "Luas Panen (ha)",
                "produktivitas": "Produktivitas (ku/ha)",
                "jumlah_produksi": "Produksi (ton)",
                "updated_at": "Terakhir Diperbarui"
            }
            tabel_tampil = data_filter[kolom_tampil].rename(columns=nama_kolom)
            with st.container(border=True):
                st.dataframe(
                    tabel_tampil,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Luas Panen (ha)": st.column_config.NumberColumn(format="%.2f"),
                        "Produktivitas (ku/ha)": st.column_config.NumberColumn(format="%.2f"),
                        "Produksi (ton)": st.column_config.NumberColumn(format="%.2f"),
                        "Terakhir Diperbarui": st.column_config.DatetimeColumn(format="DD MMM YYYY, HH:mm")
                    }
                )
                csv_data = tabel_tampil.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    "⬇️ Unduh Data Terfilter (CSV)",
                    data=csv_data,
                    file_name="data_produksi_padi_orva_sumut.csv",
                    mime="text/csv"
                )

        waktu_update = df["updated_at"].max()
        st.caption(f"Data terakhir diperbarui: {waktu_update}")

    # =====================================================
    # PENGELOLAAN DATA ADMIN
    # =====================================================
    if st.session_state.admin_logged_in:
        st.divider()
        st.markdown('<div class="section-kicker">Panel administrator</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Pengelolaan Data Produksi Padi</div>', unsafe_allow_html=True)

        menu_admin = st.selectbox(
            "Pilih Pengelolaan Data",
            ["Tambah Data", "Edit Data", "Hapus Data"]
        )

        daftar_database = {
            "Deli Serdang": "DB_DELI_SERDANG",
            "Serdang Bedagai": "DB_SERDANG_BEDAGAI",
            "Simalungun": "DB_SIMALUNGUN",
            "Tapanuli Utara": "DB_TAPANULI_UTARA",
            "Langkat": "DB_LANGKAT"
        }

        if menu_admin == "Tambah Data":
            st.subheader("➕ Tambah Data Produksi Padi")
            with st.form("form_tambah_data"):
                kabupaten = st.selectbox("Kabupaten", list(daftar_database.keys()))
                tahun = st.number_input("Tahun", min_value=2000, max_value=2100, value=2025, step=1)
                luas_panen = st.number_input("Luas Panen (ha)", min_value=0.0, step=0.01)
                produktivitas = st.number_input("Produktivitas (ku/ha)", min_value=0.0, step=0.01)
                jumlah_produksi = st.number_input("Jumlah Produksi (ton)", min_value=0.0, step=0.01)
                simpan = st.form_submit_button("Simpan Data", use_container_width=True)

            if simpan:
                try:
                    with psycopg2.connect(st.secrets[daftar_database[kabupaten]]) as conn:
                        with conn.cursor() as cursor:
                            cursor.execute("""
                                INSERT INTO produksi_padi (
                                    nama_kabupaten_kota, tahun, luas_panen,
                                    produktivitas, jumlah_produksi
                                ) VALUES (%s, %s, %s, %s, %s)
                            """, (kabupaten, int(tahun), luas_panen, produktivitas, jumlah_produksi))
                    st.success("Data berhasil disimpan!")
                    st.rerun()
                except psycopg2.errors.UniqueViolation:
                    st.error("Data kabupaten dan tahun tersebut sudah tersedia.")
                except Exception as e:
                    st.error("Gagal menyimpan data.")
                    st.caption(str(e))

        elif menu_admin == "Edit Data":
            st.subheader("✏️ Edit Data Produksi Padi")
            kabupaten_edit = st.selectbox(
                "Pilih Kabupaten", list(daftar_database.keys()), key="kabupaten_edit"
            )
            try:
                with psycopg2.connect(st.secrets[daftar_database[kabupaten_edit]]) as conn:
                    data_edit = pd.read_sql_query("""
                        SELECT id_produksi, tahun, luas_panen,
                               produktivitas, jumlah_produksi
                        FROM produksi_padi ORDER BY tahun
                    """, conn)

                if data_edit.empty:
                    st.warning("Belum ada data untuk kabupaten ini.")
                else:
                    st.dataframe(data_edit, use_container_width=True, hide_index=True)
                    id_edit = st.selectbox(
                        "Pilih ID Data yang akan diedit",
                        data_edit["id_produksi"].tolist(),
                        key="id_edit"
                    )
                    baris = data_edit[data_edit["id_produksi"] == id_edit].iloc[0]

                    with st.form("form_edit_data"):
                        tahun_baru = st.number_input(
                            "Tahun", min_value=2000, max_value=2100,
                            value=int(baris["tahun"]), step=1
                        )
                        luas_baru = st.number_input(
                            "Luas Panen (ha)", min_value=0.0,
                            value=float(baris["luas_panen"]), step=0.01
                        )
                        produktivitas_baru = st.number_input(
                            "Produktivitas (ku/ha)", min_value=0.0,
                            value=float(baris["produktivitas"]), step=0.01
                        )
                        produksi_baru = st.number_input(
                            "Jumlah Produksi (ton)", min_value=0.0,
                            value=float(baris["jumlah_produksi"]), step=0.01
                        )
                        tombol_edit = st.form_submit_button("Simpan Perubahan", use_container_width=True)

                    if tombol_edit:
                        with psycopg2.connect(st.secrets[daftar_database[kabupaten_edit]]) as conn:
                            with conn.cursor() as cursor:
                                cursor.execute("""
                                    UPDATE produksi_padi
                                    SET tahun = %s, luas_panen = %s,
                                        produktivitas = %s, jumlah_produksi = %s,
                                        updated_at = NOW()
                                    WHERE id_produksi = %s
                                """, (
                                    int(tahun_baru), luas_baru, produktivitas_baru,
                                    produksi_baru, int(id_edit)
                                ))
                        st.success("Data berhasil diperbarui!")
                        st.rerun()
            except Exception as e:
                st.error("Gagal mengedit data.")
                st.caption(str(e))

        elif menu_admin == "Hapus Data":
            st.subheader("🗑️ Hapus Data Produksi Padi")
            kabupaten_hapus = st.selectbox(
                "Pilih Kabupaten", list(daftar_database.keys()), key="kabupaten_hapus"
            )
            try:
                with psycopg2.connect(st.secrets[daftar_database[kabupaten_hapus]]) as conn:
                    data_hapus = pd.read_sql_query("""
                        SELECT id_produksi, tahun, luas_panen,
                               produktivitas, jumlah_produksi
                        FROM produksi_padi ORDER BY tahun
                    """, conn)

                if data_hapus.empty:
                    st.warning("Belum ada data untuk kabupaten ini.")
                else:
                    st.dataframe(data_hapus, use_container_width=True, hide_index=True)
                    id_hapus = st.selectbox(
                        "Pilih ID Data yang akan dihapus",
                        data_hapus["id_produksi"].tolist(),
                        key="id_hapus"
                    )
                    konfirmasi = st.checkbox("Saya yakin ingin menghapus data ini.")
                    if st.button("Hapus Data", use_container_width=True, disabled=not konfirmasi):
                        with psycopg2.connect(st.secrets[daftar_database[kabupaten_hapus]]) as conn:
                            with conn.cursor() as cursor:
                                cursor.execute(
                                    "DELETE FROM produksi_padi WHERE id_produksi = %s",
                                    (int(id_hapus),)
                                )
                        st.success("Data berhasil dihapus!")
                        st.rerun()
            except Exception as e:
                st.error("Gagal menghapus data.")
                st.caption(str(e))
    else:
        st.info("Login sebagai Admin untuk mengakses pengelolaan data.")

    st.markdown("""
    <div class="footer">
      ORVA SUMUT · Oriza Sativa Sumatera Utara<br>
      Sistem Integrasi Database Produksi Padi Sumatera Utara
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error("Terjadi kesalahan saat mengambil data.")
    st.caption(str(e))
