
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
