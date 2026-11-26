
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
# LOGIN ADMIN
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

        if st.button("Logout", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()

    st.divider()

    st.caption(
        "Hak akses: " +
        ("Admin" if st.session_state.admin_logged_in else "Pengunjung")
    )

# ==================================
# JUDUL WEBSITE
# ==================================

st.title("🌾 ORVA SUMUT")
st.subheader("Oriza Sativa Sumatera Utara")

st.write(
    "Sistem Integrasi Database Produksi Padi Sumatera Utara"
)

st.divider()

# ==================================
# KONEKSI DATABASE PUSAT
# ==================================

try:

    with psycopg2.connect(
        st.secrets["DB_PUSAT"]
    ) as conn:

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

    # ==================================
    # DASHBOARD
    # ==================================

    st.header("Dashboard Produksi Padi")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Kabupaten Terintegrasi",
            df["nama_kabupaten_kota"].nunique()
        )

    with col2:
        st.metric(
            "Total Data",
            len(df)
        )

    with col3:
        st.metric(
            "Total Produksi",
            f"{df['jumlah_produksi'].sum():,.2f} ton"
        )

    st.divider()

    # ==================================
    # FILTER DATA
    # ==================================

    st.subheader("Filter Data")

    col1, col2 = st.columns(2)

    with col1:
        pilihan_kabupaten = st.multiselect(
            "Pilih Kabupaten",
            sorted(df["nama_kabupaten_kota"].unique()),
            default=sorted(df["nama_kabupaten_kota"].unique())
        )

    with col2:
        pilihan_tahun = st.multiselect(
            "Pilih Tahun",
            sorted(df["tahun"].unique()),
            default=sorted(df["tahun"].unique())
        )

    data_filter = df[
        df["nama_kabupaten_kota"].isin(pilihan_kabupaten)
        & df["tahun"].isin(pilihan_tahun)
    ]

    # ==================================
    # GRAFIK PRODUKSI
    # ==================================

    st.subheader("Perbandingan Produksi Antar Kabupaten")

    data_grafik = (
        data_filter.groupby("nama_kabupaten_kota", as_index=False)
        ["jumlah_produksi"].sum()
    )

    fig1 = px.bar(
        data_grafik,
        x="nama_kabupaten_kota",
        y="jumlah_produksi",
        color="nama_kabupaten_kota",
        labels={
            "nama_kabupaten_kota": "Kabupaten",
            "jumlah_produksi": "Produksi (ton)"
        }
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # ==================================
    # GRAFIK PERKEMBANGAN
    # ==================================

    st.subheader("Perkembangan Produksi Padi")

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

    st.divider()

    waktu_update = df["updated_at"].max()

    st.caption(f"Data terakhir diperbarui: {waktu_update}")
    st.caption("ORVA SUMUT | Oriza Sativa Sumatera Utara")

    # ==================================
    # PENGELOLAAN DATA ADMIN
    # ==================================

    if st.session_state.admin_logged_in:

        st.divider()
        st.header("Pengelolaan Data Produksi Padi")

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

            st.subheader("Tambah Data Produksi Padi")

            with st.form("form_tambah_data"):

                kabupaten = st.selectbox(
                    "Kabupaten",
                    list(daftar_database.keys())
                )

                tahun = st.number_input(
                    "Tahun",
                    min_value=2000,
                    max_value=2100,
                    value=2025,
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

                try:
                    with psycopg2.connect(
                        st.secrets[daftar_database[kabupaten]]
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

                    st.success("Data berhasil disimpan!")
                    st.rerun()

                except psycopg2.errors.UniqueViolation:
                    st.error(
                        "Data kabupaten dan tahun tersebut sudah tersedia."
                    )

                except Exception as e:
                    st.error("Gagal menyimpan data.")
                    st.caption(str(e))

        elif menu_admin == "Edit Data":
            st.info("Fitur Edit Data akan dibuat berikutnya.")

        elif menu_admin == "Hapus Data":
            st.info("Fitur Hapus Data akan dibuat berikutnya.")

    else:
        st.info(
            "Login sebagai Admin untuk mengakses pengelolaan data."
        )

except Exception as e:
    st.error("Terjadi kesalahan saat mengambil data.")
    st.caption(str(e))
