
import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# ==================================
# KONFIGURASI HALAMAN
# ==================================

st.set_page_config(
    page_title="ORVA SUMUT",
    page_icon="🌾",
    layout="wide"
)

# ==================================
# SISTEM LOGIN PENGGUNA
# ==================================

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

with st.sidebar:
    st.title("👤 Akses Pengguna")

    if not st.session_state.admin_logged_in:

        st.info("Mode Pengunjung")

        with st.form("login_admin"):
            password = st.text_input(
                "Password Admin",
                type="password"
            )

            login_button = st.form_submit_button(
                "Masuk sebagai Admin",
                use_container_width=True
            )

        if login_button:
            if password == st.secrets["ADMIN_PASSWORD"]:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Password tidak sesuai.")

    else:
        st.success("Login sebagai Admin")

        if st.button(
            "Logout",
            use_container_width=True
        ):
            st.session_state.admin_logged_in = False
            st.rerun()

    st.divider()

    if st.session_state.admin_logged_in:
        st.caption("Hak akses: Admin")
    else:
        st.caption("Hak akses: Pengunjung")

# ==================================
# HEADER
# ==================================

st.title("🌾 ORVA SUMUT")
st.subheader("Oriza Sativa Sumatera Utara")

st.caption(
    "Sistem Integrasi Database Produksi Padi Sumatera Utara"
)

st.divider()

# ==================================
# KONEKSI DATABASE
# ==================================

try:
    db_url = st.secrets["DB_PUSAT"]

    with psycopg2.connect(db_url) as conn:
        df = pd.read_sql_query(
            """
            SELECT
                nama_kabupaten_kota,
                tahun,
                luas_panen,
                produktivitas,
                jumlah_produksi,
                updated_at
            FROM produksi_padi
            ORDER BY nama_kabupaten_kota, tahun;
            """,
            conn
        )

    # Memastikan tipe data numerik
    for kolom in [
        "luas_panen",
        "produktivitas",
        "jumlah_produksi"
    ]:
        df[kolom] = pd.to_numeric(
            df[kolom], errors="coerce"
        )

    if df.empty:
        st.warning("Belum ada data produksi padi.")
        st.stop()

    # ==================================
    # FILTER DATA
    # ==================================

    st.header("Dashboard Produksi Padi")

    col_filter1, col_filter2 = st.columns(2)

    daftar_kabupaten = ["Semua Kabupaten"] + sorted(
        df["nama_kabupaten_kota"].dropna().unique().tolist()
    )

    daftar_tahun = ["Semua Tahun"] + sorted(
        df["tahun"].dropna().unique().tolist()
    )

    with col_filter1:
        kabupaten = st.selectbox(
            "Pilih Kabupaten",
            daftar_kabupaten
        )

    with col_filter2:
        tahun = st.selectbox(
            "Pilih Tahun",
            daftar_tahun
        )

    # Menerapkan filter
    data_filter = df.copy()

    if kabupaten != "Semua Kabupaten":
        data_filter = data_filter[
            data_filter["nama_kabupaten_kota"] == kabupaten
        ]

    if tahun != "Semua Tahun":
        data_filter = data_filter[
            data_filter["tahun"] == tahun
        ]

    # ==================================
    # RINGKASAN DATA
    # ==================================

    st.subheader("Ringkasan Produksi")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Kabupaten Terintegrasi",
        data_filter["nama_kabupaten_kota"].nunique()
    )

    col2.metric(
        "Total Data",
        len(data_filter)
    )

    total_produksi = data_filter[
        "jumlah_produksi"
    ].sum()

    col3.metric(
        "Total Produksi",
        f"{total_produksi:,.2f} ton"
    )

    st.divider()

    # ==================================
    # GRAFIK PRODUKSI PER KABUPATEN
    # ==================================

    st.subheader("Perbandingan Produksi Antar Kabupaten")

    produksi_kabupaten = (
        data_filter.groupby("nama_kabupaten_kota", as_index=False)
        ["jumlah_produksi"].sum()
    )

    fig1 = px.bar(
        produksi_kabupaten,
        x="nama_kabupaten_kota",
        y="jumlah_produksi",
        color="nama_kabupaten_kota",
        text_auto=".2s",
        labels={
            "nama_kabupaten_kota": "Kabupaten",
            "jumlah_produksi": "Produksi (ton)"
        }
    )

    fig1.update_layout(
        showlegend=False,
        xaxis_title="Kabupaten",
        yaxis_title="Produksi (ton)"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ==================================
    # GRAFIK PERKEMBANGAN PRODUKSI
    # ==================================

    st.subheader("Perkembangan Produksi Padi")

    produksi_tahun = (
        data_filter.groupby("tahun", as_index=False)
        ["jumlah_produksi"].sum()
        .sort_values("tahun")
    )

    fig2 = px.line(
        produksi_tahun,
        x="tahun",
        y="jumlah_produksi",
        markers=True,
        text="jumlah_produksi",
        labels={
            "tahun": "Tahun",
            "jumlah_produksi": "Produksi (ton)"
        }
    )

    fig2.update_layout(
        xaxis_title="Tahun",
        yaxis_title="Produksi (ton)"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ==================================
    # TABEL DATA
    # ==================================

    st.subheader("Data Produksi Padi")

    st.dataframe(
        data_filter,
        use_container_width=True,
        hide_index=True
    )

    # ==================================
    # INFORMASI SISTEM
    # ==================================

    st.divider()

    waktu_update = df["updated_at"].max()

    st.caption(
        f"Data terakhir diperbarui: {waktu_update}"
    )

    st.caption(
        "ORVA SUMUT | Oriza Sativa Sumatera Utara"
    )
        # ==================================
    # PENGELOLAAN DATA ADMIN
    # ==================================

    if st.session_state.admin_logged_in:

        st.divider()
        st.header("Pengelolaan Data Produksi Padi")

        menu_admin = st.selectbox(
            "Pilih Pengelolaan Data",
            [
                "Tambah Data",
                "Edit Data",
                "Hapus Data"
            ]
        )
                if menu_admin == "Tambah Data":

            st.subheader("Tambah Data Produksi Padi")

            daftar_database = {
                "Deli Serdang": "DB_DELI_SERDANG",
                "Serdang Bedagai": "DB_SERDANG_BEDAGAI",
                "Simalungun": "DB_SIMALUNGUN",
                "Tapanuli Utara": "DB_TAPANULI_UTARA",
                "Langkat": "DB_LANGKAT"
            }

            with st.form("form_tambah_data"):

                kabupaten = st.selectbox(
                    "Kabupaten",
                    list(daftar_database.keys())
                )

                tahun = st.number_input(
                    "Tahun",
                    min_value=2000,
                    max_value=2100,
                    step=1
                )

                luas_panen = st.number_input(
                    "Luas Panen (ha)",
                    min_value=0.0,
                    step=0.01
                )

                produktivitas = st.number_input(
                    "Produktivitas (ku/ha)",
                    min_value=0.0,
                    step=0.01
                )

                jumlah_produksi = st.number_input(
                    "Jumlah Produksi (ton)",
                    min_value=0.0,
                    step=0.01
                )

                simpan = st.form_submit_button(
                    "Simpan Data",
                    use_container_width=True
                )

            if simpan:

                secret_name = daftar_database[kabupaten]

                try:
                    with psycopg2.connect(
                        st.secrets[secret_name]
                    ) as conn:

                        with conn.cursor() as cursor:

                            cursor.execute("""
                                INSERT INTO produksi_padi (
                                    nama_kabupaten_kota,
                                    tahun,
                                    luas_panen,
                                    produktivitas,
                                    jumlah_produksi
                                )
                                VALUES (%s, %s, %s, %s, %s)
                            """, (
                                kabupaten,
                                int(tahun),
                                luas_panen,
                                produktivitas,
                                jumlah_produksi
                            ))

                    st.success(
                        f"Data produksi {kabupaten} tahun {int(tahun)} berhasil disimpan!"
                    )

                    st.rerun()

                except psycopg2.errors.UniqueViolation:
                    st.error(
                        "Data untuk kabupaten dan tahun tersebut sudah tersedia."
                    )

                except Exception as e:
                    st.error("Gagal menyimpan data.")
                    st.caption(str(e))

        st.info(
            "Menu ini hanya dapat digunakan oleh pengguna dengan akses Admin."
        )

    else:
        st.info(
            "Login sebagai Admin untuk mengakses fitur pengelolaan data."
        )

except Exception as e:
    st.error("Terjadi kesalahan saat mengambil data.")
    st.caption(str(e))
