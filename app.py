import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistem Data Pelajar APDM", layout="wide")

# Header Ringkas Tanpa CSS Rumit
st.title("SISTEM MAKLUMAT PELAJAR BERPUSAT")
st.write("### NEE4099 | SMK RANTAU")
st.markdown("---")

if 'df_pelajar' not in st.session_state:
    st.session_state['df_pelajar'] = None

st.sidebar.title("Navigasi Sistem")
pilihan_page = st.sidebar.radio("Pergi ke:", ["Page 1: Muat Naik Fail", "Page 2: Carian Murid", "Page 3: Cetak Laporan"])

# ==========================================
# PAGE 1: MUAT NAIK FAIL
# ==========================================
if pilihan_page == "Page 1: Muat Naik Fail":
    st.subheader("📁 Muat Naik Database Pelajar (Excel / CSV APDM)")
    fail_dimuat_naik = st.file_uploader("Pilih fail database anda:", type=["csv", "xlsx"])
    
    if fail_dimuat_naik is not None:
        try:
            if fail_dimuat_naik.name.endswith('.csv'):
                df = pd.read_csv(fail_dimuat_naik)
            else:
                df = pd.read_excel(fail_dimuat_naik)
            
            st.session_state['df_pelajar'] = df
            st.success(f"Berjaya! {len(df)} rekod pelajar dikesan.")
            st.dataframe(df.head(5))
        except Exception as e:
            st.error(f"Ralat membaca fail: {e}")
    else:
        st.info("Sila muat naik fail CSV/Excel eksport APDM anda yang mengandungi data murid.")

# ==========================================
# PAGE 2: DROPDOWN PILIH KELAS & MURID
# ==========================================
elif pilihan_page == "Page 2: Carian Murid":
    st.subheader("🔍 Carian Maklumat Pelajar")
    if st.session_state['df_pelajar'] is None:
        st.warning("⚠️ Sila muat naik fail database di Page 1 terlebih dahulu.")
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
            st.success(f"Murid dipilih: {murid_dipilih}. Sila ke Page 3.")

# ==========================================
# PAGE 3: PORTRAIT REPORT
# ==========================================
elif pilihan_page == "Page 3: Cetak Laporan":
    if 'murid_terpilih' not in st.session_state or st.session_state['df_pelajar'] is None:
        st.warning("⚠️ Sila pilih murid di Page 2 terlebih dahulu.")
    else:
        m = st.session_state['murid_terpilih']
        
        if st.button("🖨️ Cetak Laporan (Guna fungsi Print Pelayar Web)"):
            st.components.v1.html("<script>window.print();</script>", height=1)
            
        st.write(f"## LAPORAN PROFIL MURID - SMK RANTAU")
        st.write(f"**Nama Penuh:** {m.get('NAMA', 'N/A')}")
        st.write(f"**ID Murid:** {m.get('ID MURID', 'N/A')}")
        st.write(f"**No. Kad Pengenalan:** {m.get('NO. PENGENALAN', 'N/A')}")
        st.write(f"**Kelas:** {m.get('NAMA KELAS', 'N/A')}")
        st.write(f"**Jantina:** {m.get('JANTINA', 'N/A')}")
        st.write(f"**Kaum / Agama:** {m.get('KAUM', 'N/A')} / {m.get('AGAMA', 'N/A')}")
        st.write(f"**Penjaga 1:** {m.get('PENJAGA 1', 'N/A')} ({m.get('HUBUNGAN PENJAGA 1', 'N/A')})")
        st.write(f"**No. Tel Penjaga 1:** {m.get('NO. TEL. BIMBIT PENJAGA 1', 'N/A')}")
