import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman & CSS Khas untuk Cetakan PDF
st.set_page_config(page_title="Sistem Data Pelajar APDM", layout="wide")

st.markdown("""
    <style>
    /* Rekabentuk Header Biru Rasmi */
    .official-header {
        background-color: #0056b3;
        color: white;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .school-info {
        font-weight: bold;
        font-size: 14px;
        margin-top: 5px;
        letter-spacing: 1px;
    }
    
    /* CSS Khas untuk Cetakan Cetak ke PDF (3 Muka Surat Portrait) */
    @media print {
        body * {
            visibility: hidden;
        }
        .print-container, .print-container * {
            visibility: visible;
        }
        .print-container {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
        }
        .page-break {
            page-break-after: always;
            break-after: page;
            height: 100vh;
            padding-top: 20px;
        }
        .no-print {
            display: none !important;
        }
    }
    </style>
""", unsafe_allowed_html=True)

def papar_header():
    st.markdown("""
        <div class="official-header">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 45px; margin-right: 20px;">🏫</div>
                <div>
                    <h2 style="margin: 0; color: white; font-family: 'Helvetica Neue', Arial, sans-serif;">SISTEM MAKLUMAT PELAJAR BERPUSAT</h2>
                    <div class="school-info">NEE4099 | SMK RANTAU</div>
                </div>
            </div>
        </div>
    """, unsafe_allowed_html=True)

if 'df_pelajar' not in st.session_state:
    st.session_state['df_pelajar'] = None

st.sidebar.title("Navigasi Sistem")
pilihan_page = st.sidebar.radio("Pergi ke:", ["Page 1: Muat Naik Fail", "Page 2: Carian Murid", "Page 3: Cetak Laporan"])

# ==========================================
# PAGE 1: MUAT NAIK FAIL
# ==========================================
if pilihan_page == "Page 1: Muat Naik Fail":
    papar_header()
    st.subheader("📁 Muat Naik Database Pelajar (Excel / CSV APDM)")
    
    fail_dimuat_naik = st.file_uploader("Pilih fail database anda:", type=["csv", "xlsx"])
    
    if fail_dimuat_naik is not None:
        try:
            if fail_dimuat_naik.name.endswith('.csv'):
                df = pd.read_csv(fail_dimuat_naik)
            else:
                df = pd.read_excel(fail_dimuat_naik)
            
            st.session_state['df_pelajar'] = df
            st.success(f"Berjaya! {len(df)} rekod pelajar dikesan daripada fail APDM.")
            
            st.write("### Pratinjau Data:")
            st.dataframe(df.head(5))
            
        except Exception as e:
            st.error(f"Ralat membaca fail: {e}")
    else:
        st.info("Sila muat naik fail CSV/Excel eksport APDM anda yang mengandungi data murid.")

# ==========================================
# PAGE 2: DROPDOWN PILIH KELAS & MURID
# ==========================================
elif pilihan_page == "Page 2: Carian Murid":
    papar_header()
    st.subheader("🔍 Carian Maklumat Pelajar")
    
    if st.session_state['df_pelajar'] is None:
        st.warning("⚠️ Sila muat naik fail database di **Page 1** terlebih dahulu.")
    else:
        df = st.session_state['df_pelajar']
        
        df['NAMA KELAS'] = df['NAMA KELAS'].astype(str)
        df['NAMA'] = df['NAMA'].astype(str)
        
        senarai_kelas = sorted(df['NAMA KELAS'].unique())
        kelas_dipilih = st.selectbox("1. Pilih Kelas:", senarai_kelas)
        
        df_tapis_kelas = df[df['NAMA KELAS'] == kelas_dipilih]
        
        senarai_murid = sorted(df_tapis_kelas['NAMA'].unique())
        murid_dipilih = st.selectbox("2. Pilih Nama Murid:", senarai_murid)
        
        if murid_dipilih:
            data_murid = df_tapis_kelas[df_tapis_kelas['NAMA'] == murid_dipilih].iloc[0]
            st.session_state['murid_terpilih'] = data_murid
            st.success(f"Murid dipilih: {murid_dipilih}. Sila ke **Page 3** untuk cetakan.")

# ==========================================
# PAGE 3: PORTRAIT REPORT (SMK RANTAU)
# ==========================================
elif pilihan_page == "Page 3: Cetak Laporan":
    papar_header()
    
    if 'murid_terpilih' not in st.session_state or st.session_state['df_pelajar'] is None:
        st.warning("⚠️ Sila pilih murid di **Page 2** terlebih dahulu.")
    else:
        m = st.session_state['murid_terpilih']
        
        st.markdown("""
            <div class="no-print" style="margin-bottom: 20px;">
                <p>💡 <i>Tip Cetakan: Pilih 'Save as PDF', Layout: 'Portrait', dan hidupkan 'Background graphics'.</i></p>
            </div>
        """, unsafe_allowed_html=True)
        
        if st.button("🖨️ Cetak / Simpan ke PDF"):
            st.components.v1.html("<script>window.print();</script>", height=1)
            
        st.markdown(f"""
        <div class="print-container">
            
            <div class="page-break">
                <div style="border-bottom: 3px double #000; padding-bottom: 10px; margin-bottom: 30px; text-align: center;">
                    <h2>LAPORAN PROFIL MURID (MUKA SURAT 1/3)</h2>
                    <p><b>SMK RANTAU (NEE4099)</b></p>
                </div>
                <h3>BAHAGIAN A: PROFIL AKADEMIK & SEKOLAH</h3>
                <table style="width:100%; border-collapse: collapse; margin-top: 15px;">
                    <tr><td style="padding: 10px; border: 1px solid #ddd; width: 30%; font-weight:bold;">Nama Penuh</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('NAMA', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; width: 30%; font-weight:bold;">ID Murid</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('ID MURID', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">No. Kad Pengenalan</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('NO. PENGENALAN', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Tingkatan / Kelas</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('NAMA KELAS', 'N/A')} ({m.get('TAHUN / TINGKATAN', 'N/A')})</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Guru Kelas</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('NAMA GURU KELAS', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Aliran / Bidang</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('KETERANGAN ALIRAN', 'N/A')} - {m.get('KETERANGAN BIDANG', 'N/A')}</td></tr>
                </table>
                <br>
                <h3>BAHAGIAN B: BIODATA DIRI</h3>
                <table style="width:100%; border-collapse: collapse; margin-top: 15px;">
                    <tr><td style="padding: 10px; border: 1px solid #ddd; width: 30%; font-weight:bold;">Tarikh Lahir</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('TARIKH LAHIR', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Jantina</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('JANTINA', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Kaum / Agama</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('KAUM', 'N/A')} / {m.get('AGAMA', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Warganegara</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('WARGANEGARA', 'N/A')}</td></tr>
                </table>
            </div>
            
            <div class="page-break">
                <div style="border-bottom: 3px double #000; padding-bottom: 10px; margin-bottom: 30px; text-align: center;">
                    <h2>LAPORAN PROFIL MURID (MUKA SURAT 2/3)</h2>
                    <p><b>SMK RANTAU (NEE4099)</b></p>
                </div>
                <h3>BAHAGIAN C: MAKLUMAT PENJAGA UTAMA (PENJAGA 1)</h3>
                <table style="width:100%; border-collapse: collapse; margin-top: 15px;">
                    <tr><td style="padding: 10px; border: 1px solid #ddd; width: 30%; font-weight:bold;">Nama Penjaga 1</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('PENJAGA 1', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">No. KP Penjaga 1</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('NO. PENGENALAN PENJAGA 1', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Hubungan</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('HUBUNGAN PENJAGA 1', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Pekerjaan</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('PEKERJAAN PENJAGA 1', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Pendapatan Bulanan</td><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold; color: #b30000;">RM {m.get('PENDAPATAN PENJAGA 1', '0')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">No. Telefon Bimbit</td><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">{m.get('NO. TEL. BIMBIT PENJAGA 1', 'N/A')}</td></tr>
                </table>
            </div>
            
            <div class="page-break">
                <div style="border-bottom: 3px double #000; padding-bottom: 10px; margin-bottom: 30px; text-align: center;">
                    <h2>LAPORAN PROFIL MURID (MUKA SURAT 3/3)</h2>
                    <p><b>SMK RANTAU (NEE4099)</b></p>
                </div>
                <h3>BAHAGIAN D: STATUS KEBAJIKAN & ASRAMA</h3>
                <table style="width:100%; border-collapse: collapse; margin-top: 15px;">
                    <tr><td style="padding: 10px; border: 1px solid #ddd; width: 30%; font-weight:bold;">Status Asrama</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('STATUS ASRAMA', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Status OKU</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('STATUS OKU', 'TIDAK')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Status Anak Yatim</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('STATUS YATIM', 'TIDAK')}</td></tr>
                </table>
                <br><br>
                <h3>BAHAGIAN E: ULASAN GURU KELAS & SAHSIAH</h3>
                <div style="border: 1px solid #ddd; padding: 20px; border-radius: 5px; background: #fff; min-height: 120px; color: #555;">
                    ........................................................................................................................................................................
                </div>
                <br><br><br>
                <div style="display: flex; justify-content: space-between; margin-top: 50px;">
                    <div style="text-align: center; width: 40%;">
                        <p>___________________________</p>
                        <p>(Tandatangan Guru Kelas)</p>
                    </div>
                    <div style="text-align: center; width: 40%;">
                        <p>___________________________</p>
                        <p>(Tandatangan Pengetua / PK HEM)</p>
                    </div>
                </div>
            </div>
            
        </div>
        """, unsafe_allowed_html=True)            <div style="display: flex; align-items: center;">
                <div style="font-size: 45px; margin-right: 20px;">🏫</div>
                <div>
                    <h2 style="margin: 0; color: white; font-family: 'Helvetica Neue', Arial, sans-serif;">SISTEM MAKLUMAT PELAJAR BERPUSAT</h2>
                    <div class="school-info">NEE4099 | SMK RANTAU</div>
                </div>
            </div>
        </div>
    """, unsafe_allowed_html=True)

# 3. Pengurusan Session State
if 'df_pelajar' not in st.session_state:
    st.session_state['df_pelajar'] = None

# 4. Navigasi Landing Page
st.sidebar.title("Navigasi Sistem")
pilihan_page = st.sidebar.radio("Pergi ke:", ["Page 1: Muat Naik Fail", "Page 2: Carian Murid", "Page 3: Cetak Laporan"])

# ==========================================
# PAGE 1: MUAT NAIK FAIL
# ==========================================
if pilihan_page == "Page 1: Muat Naik Fail":
    papar_header()
    st.subheader("📁 Muat Naik Database Pelajar (Excel / CSV)")
    
    fail_dimuat_naik = st.file_uploader("Pilih fail database anda:", type=["csv", "xlsx"])
    
    # DI SINI TELAH DIBETULKAN: Menggunakan 'None' menggantikan 'nil'
    if fail_dimuat_naik is not None:
        try:
            if fail_dimuat_naik.name.endswith('.csv'):
                df = pd.read_csv(fail_dimuat_naik)
            else:
                df = pd.read_excel(fail_dimuat_naik)
            
            st.session_state['df_pelajar'] = df
            st.success(f"Berjaya memuat naik fail! {len(df)} rekod pelajar dikesan.")
            
            st.write("### Pratinjau Data:")
            st.dataframe(df.head(5))
            
        except Exception as e:
            st.error(f"Ralat membaca fail: {e}")
    else:
        st.info("Sila muat naik fail yang mengandungi kolum minima: **Nama, MyKad, Kelas, Jantina, Kaum, Agama, Nama Penjaga, No Tel Penjaga, Alamat, Kehadiran, PNGK, Catatan**")

# ==========================================
# PAGE 2: DROPDOWN PILIH KELAS & MURID
# ==========================================
elif pilihan_page == "Page 2: Carian Murid":
    papar_header()
    st.subheader("🔍 Carian Maklumat Pelajar")
    
    if st.session_state['df_pelajar'] is None:
        st.warning("⚠️ Sila muat naik fail database di **Page 1** terlebih dahulu sebelum membuat carian.")
    else:
        df = st.session_state['df_pelajar']
        
        df['Kelas'] = df['Kelas'].astype(str)
        df['Nama'] = df['Nama'].astype(str)
        
        senarai_kelas = sorted(df['Kelas'].unique())
        kelas_dipilih = st.selectbox("1. Pilih Kelas:", senarai_kelas)
        
        df_tapis_kelas = df[df['Kelas'] == kelas_dipilih]
        
        senarai_murid = sorted(df_tapis_kelas['Nama'].unique())
        murid_dipilih = st.selectbox("2. Pilih Nama Murid:", senarai_murid)
        
        if murid_dipilih:
            data_murid = df_tapis_kelas[df_tapis_kelas['Nama'] == murid_dipilih].iloc[0]
            st.session_state['murid_terpilih'] = data_murid
            st.success(f"Murid dipilih: {murid_dipilih}. Sila ke **Page 3** untuk melihat dan mencetak laporan.")

# ==========================================
# PAGE 3: PORTRAIT REPORT & BUTTON PRINT
# ==========================================
elif pilihan_page == "Page 3: Cetak Laporan":
    papar_header()
    
    if 'murid_terpilih' not in st.session_state or st.session_state['df_pelajar'] is None:
        st.warning("⚠️ Tiada rekod murid dipilih. Sila pilih murid di **Page 2** terlebih dahulu.")
    else:
        m = st.session_state['murid_terpilih']
        
        st.markdown("""
            <div class="no-print" style="margin-bottom: 20px;">
                <p>💡 <i>Tip: Sila pastikan tetapan cetakan pelayar anda memilih 'Save as PDF', Layout: 'Portrait', dan hidupkan 'Background graphics'.</i></p>
            </div>
        """, unsafe_allowed_html=True)
        
        if st.button("🖨️ Cetak / Simpan ke PDF"):
            st.components.v1.html("<script>window.print();</script>", height=1)
            
        st.markdown(f"""
        <div class="print-container">
            
            <div class="page-break">
                <div style="border-bottom: 3px double #000; padding-bottom: 10px; margin-bottom: 30px; text-align: center;">
                    <h2>LAPORAN PROFIL MURID (MUKA SURAT 1/3)</h2>
                    <p><b>SMK RANTAU (NEE4099)</b></p>
                </div>
                <h3>BAHAGIAN A: MAKLUMAT PERIBADI</h3>
                <table style="width:100%; border-collapse: collapse; margin-top: 15px;">
                    <tr><td style="padding: 10px; border: 1px solid #ddd; width: 30%; font-weight:bold;">Nama Penuh</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('Nama', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">No. MyKad / ID</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('MyKad', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Kelas</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('Kelas', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Jantina</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('Jantina', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Kaum</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('Kaum', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">Agama</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('Agama', 'N/A')}</td></tr>
                </table>
                <br><br>
                <h3>BAHAGIAN B: ALAMAT RUMAH</h3>
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; background: #fff;">
                    {m.get('Alamat', 'N/A')}
                </div>
            </div>
            
            <div class="page-break">
                <div style="border-bottom: 3px double #000; padding-bottom: 10px; margin-bottom: 30px; text-align: center;">
                    <h2>LAPORAN PROFIL MURID (MUKA SURAT 2/3)</h2>
                    <p><b>SMK RANTAU (NEE4099)</b></p>
                </div>
                <h3>BAHAGIAN C: DATA PENJAGA UTAMA</h3>
                <table style="width:100%; border-collapse: collapse; margin-top: 15px;">
                    <tr><td style="padding: 10px; border: 1px solid #ddd; width: 30%; font-weight:bold;">Nama Penjaga</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('Nama Penjaga', 'N/A')}</td></tr>
                    <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight:bold;">No. Telefon</td><td style="padding: 10px; border: 1px solid #ddd;">{m.get('No Tel Penjaga', 'N/A')}</td></tr>
                </table>
                <br><br>
                <h3>BAHAGIAN D: REKOD KEHADIRAN SEKOLAH</h3>
                <table style="width:100%; border-collapse: collapse; margin-top: 15px;">
                    <tr><td style="padding: 10px; border: 1px solid #ddd; width: 30%; font-weight:bold;">Peratus Kehadiran</td><td style="padding: 10px; border: 1px solid #ddd; font-size: 18px; color: green; font-weight: bold;">{m.get('Kehadiran', 'N/A')}</td></tr>
                </table>
            </div>
            
            <div class="page-break">
                <div style="border-bottom: 3px double #000; padding-bottom: 10px; margin-bottom: 30px; text-align: center;">
                    <h2>LAPORAN PROFIL MURID (MUKA SURAT 3/3)</h2>
                    <p><b>SMK RANTAU (NEE4099)</b></p>
                </div>
                <h3>BAHAGIAN E: PRESTASI AKADEMIK</h3>
                <table style="width:100%; border-collapse: collapse; margin-top: 15px;">
                    <tr><td style="padding: 10px; border: 1px solid #ddd; width: 30%; font-weight:bold;">Pencapaian semasa (PNGK / Gred)</td><td style="padding: 10px; border: 1px solid #ddd; font-size: 18px; font-weight: bold;">{m.get('PNGK', 'N/A')}</td></tr>
                </table>
                <br><br>
                <h3>BAHAGIAN F: ULASAN / CATATAN GURU KELAS</h3>
                <div style="border: 1px solid #ddd; padding: 20px; border-radius: 5px; background: #fff; min-height: 150px;">
                    {m.get('Catatan', 'Tiada ulasan dimasukkan.')}
                </div>
                <br><br><br><br>
                <div style="display: flex; justify-content: space-between; margin-top: 50px;">
                    <div style="text-align: center; width: 40%;">
                        <p>___________________________</p>
                        <p>(Tandatangan Guru Kelas)</p>
                    </div>
                    <div style="text-align: center; width: 40%;">
                        <p>___________________________</p>
                        <p>(Tandatangan Pengetua / PK HEM)</p>
                    </div>
                </div>
            </div>
            
        </div>
        """, unsafe_allowed_html=True)
