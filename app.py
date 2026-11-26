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
                            FROM produksi_padi
                            ORDER BY tahun
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
                                        SET tahun = %s,
                                            luas_panen = %s,
                                            produktivitas = %s,
                                            jumlah_produksi = %s,
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
                            FROM produksi_padi
                            ORDER BY tahun
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
          <strong>🌾 ORVA SUMUT</strong><br>
          Oriza Sativa Sumatera Utara · Sistem Integrasi Database Produksi Padi<br>
          <span style="color:#9AA79F;">Data terakhir ditampilkan berdasarkan database pusat.</span>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error("Terjadi kesalahan saat mengambil data.")
    st.caption(str(e))
