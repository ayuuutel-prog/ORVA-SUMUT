
import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(
    page_title="ORVA SUMUT",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 ORVA SUMUT")
st.subheader("Oriza Sativa Sumatera Utara")

st.write(
    "Sistem Integrasi Database Produksi Padi "
    "Sumatera Utara"
)

st.divider()

st.header("Dashboard Produksi Padi")

try:
    db_url = st.secrets["DB_PUSAT"]

    conn = psycopg2.connect(db_url)

    query = """
        SELECT
            nama_kabupaten_kota,
            tahun,
            luas_panen,
            produktivitas,
            jumlah_produksi,
            updated_at
        FROM produksi_padi
        ORDER BY nama_kabupaten_kota, tahun;
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Kabupaten Terintegrasi",
        df["nama_kabupaten_kota"].nunique()
    )

    col2.metric(
        "Total Data",
        len(df)
    )

    col3.metric(
        "Total Produksi",
        f"{df['jumlah_produksi'].sum():,.2f} ton"
    )

    st.divider()

    st.subheader("Data Produksi Padi")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

except KeyError:
    st.warning(
        "Koneksi database belum dikonfigurasi. "
        "Silakan atur DB_PUSAT pada Streamlit Secrets."
    )

except Exception:
    st.error(
        "Belum berhasil mengambil data dari database. "
        "Periksa konfigurasi koneksi."
    )

st.divider()

st.caption(
    "ORVA SUMUT | Sistem Informasi Produksi Padi Sumatera Utara"
)
