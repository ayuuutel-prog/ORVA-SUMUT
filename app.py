
import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="ORVA SUMUT",
    page_icon="🌾",
    layout="wide"
)

# Identitas sistem
st.title("🌾 ORVA SUMUT")
st.subheader("Oriza Sativa Sumatera Utara")

st.markdown(
    """
    **Sistem Integrasi Database Produksi Padi Sumatera Utara**

    Platform digital untuk mengintegrasikan, menyajikan,
    dan mengelola data produksi padi dari berbagai kabupaten
    di Sumatera Utara secara terpusat.
    """
)

st.divider()

# Ringkasan dashboard
st.header("Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Kabupaten Terintegrasi", "5")
col2.metric("Total Data", "10")
col3.metric("Periode Data", "2023–2024")

st.divider()

# Menu informasi
st.header("Informasi Sistem")

st.info(
    "ORVA SUMUT menghubungkan lima database daerah "
    "ke dalam satu database pusat melalui proses "
    "sinkronisasi otomatis."
)

st.caption("ORVA SUMUT | Sistem Informasi Produksi Padi Sumatera Utara")
