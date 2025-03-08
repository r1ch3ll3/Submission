import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Load dataset
hour_df = pd.read_csv("data\hour.csv")
day_df = pd.read_csv("data\day.csv")

# Konversi tanggal
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# --- Sidebar ---
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Tanggal Mulai", hour_df["dteday"].min())
end_date = st.sidebar.date_input("Tanggal Akhir", hour_df["dteday"].max())

# Filter data
hour_df = hour_df[(hour_df["dteday"] >= pd.to_datetime(start_date)) & (hour_df["dteday"] <= pd.to_datetime(end_date))]
day_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & (day_df["dteday"] <= pd.to_datetime(end_date))]

# --- Main Page ---
st.title("Bike Sharing Dashboard")

# --- Pertanyaan 1: Pengaruh Cuaca ---
st.header("Pengaruh Cuaca terhadap Penyewaan Sepeda")

# Data preparation
cuaca_hari_kerja = hour_df[hour_df['workingday'] == 1].groupby('weathersit')['cnt'].mean()
cuaca_hari_libur = hour_df[hour_df['holiday'] == 0].groupby('weathersit')['cnt'].mean()
cuaca_pengaruh_df = pd.DataFrame({'Hari Kerja': cuaca_hari_kerja, 'Hari Libur': cuaca_hari_libur})
cuaca_pengaruh_df.index = ['Cerah', 'Mendung', 'Hujan Ringan', 'Cuaca Buruk']

# Visualisasi
fig1, ax1 = plt.subplots(figsize=(10, 6))
cuaca_pengaruh_df.plot(kind='bar', ax=ax1)
ax1.set_title('Pengaruh Cuaca terhadap Penyewaan Sepeda')
ax1.set_xlabel('Kondisi Cuaca (weathersit)')
ax1.set_ylabel('Rata-rata Penyewaan')
ax1.tick_params(axis='x', rotation=0)
st.pyplot(fig1)

# Insight
st.markdown("""
**Insight:**
- Cuaca Cerah Paling Diminati: Kondisi cuaca cerah (Cerah) memiliki rata-rata penyewaan sepeda tertinggi, baik pada hari kerja maupun hari libur.
- Cuaca Buruk Kurangi Penyewaan: Kondisi cuaca buruk (Cuaca Buruk) memiliki rata-rata penyewaan sepeda terendah, baik pada hari kerja maupun hari libur.
- Hari Kerja Sedikit Lebih Tinggi: Rata-rata penyewaan sepeda pada hari kerja sedikit lebih tinggi dibandingkan hari libur di semua kondisi cuaca.
- Pengaruh Cuaca Konsisten: Pola pengaruh cuaca terhadap penyewaan sepeda relatif konsisten antara hari kerja dan hari libur.
- Perbedaan Signifikan: Terdapat perbedaan signifikan dalam rata-rata penyewaan antara kondisi cuaca cerah dan kondisi cuaca buruk.
""")

# --- Pertanyaan 2: Tren Bulanan ---
st.header("Tren Penyewaan Sepeda Setiap Bulan")

# Data preparation
monthly_rentals = hour_df.groupby('mnth')['cnt'].sum()

# Visualisasi
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(monthly_rentals.index, monthly_rentals.values, marker='o')
ax2.set_title('Tren Penyewaan Sepeda Setiap Bulan')
ax2.set_xlabel('Bulan')
ax2.set_ylabel('Total Penyewaan')
ax2.set_xticks(range(1, 13))
ax2.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
ax2.grid(True)
st.pyplot(fig2)

# Insight
st.markdown("""
**Insight:**
- Puncak Musim Panas: Jumlah penyewaan sepeda mencapai puncaknya pada bulan-bulan musim panas, khususnya Juni, Juli, dan Agustus.
- Musim Dingin Sepi Peminat: Jumlah penyewaan sepeda terendah terjadi pada bulan-bulan musim dingin, yaitu Januari dan Februari.
- Tren Meningkat Stabil: Terdapat tren peningkatan stabil dalam penyewaan sepeda dari bulan Januari hingga Agustus.
- Tren Menurun Stabil: Setelah puncak di bulan Agustus, terjadi tren penurunan stabil dalam penyewaan sepeda hingga bulan Desember.
- Pola Musiman yang Jelas: Grafik menunjukkan pola musiman yang jelas, dengan fluktuasi signifikan antara bulan-bulan musim panas dan musim dingin.
""")

# --- Analisis Lanjutan: Kategori Cuaca ---
st.header("Analisis Pengaruh Cuaca dan Kecepatan Angin terhadap Penggunaan Sepeda (Hari Kerja vs. Hari Libur)")

# Fungsi kategori cuaca
def kategori_cuaca(row):
    if row['atemp'] > 0.6 and row['hum'] < 0.4 and row['windspeed'] < 0.3:
        return 'Cerah & Hangat'
    elif row['atemp'] < 0.3 and row['hum'] > 0.7 and row['windspeed'] > 0.5:
        return 'Hujan & Dingin'
    elif row['atemp'] < 0.5 and row['hum'] > 0.6 and row['windspeed'] < 0.4:
        return 'Mendung & Dingin'
    elif row['atemp'] > 0.6 and row['hum'] > 0.6 and row['windspeed'] < 0.3:
        return 'Mendung & Hangat'
    else:
        return 'Lainnya'

hour_df['kondisi_cuaca'] = hour_df.apply(kategori_cuaca, axis=1)

# Data preparation
cuaca_hari_kerja_kategori = hour_df[hour_df['workingday'] == 1].groupby('kondisi_cuaca')['cnt'].mean()
cuaca_akhir_pekan_kategori = hour_df[hour_df['holiday'] == 0].groupby('kondisi_cuaca')['cnt'].mean()

# Visualisasi
fig3, ax3 = plt.subplots(figsize=(12, 6))
cuaca_hari_kerja_kategori.plot(kind='bar', alpha=0.7, label='Hari Kerja', ax=ax3)
cuaca_akhir_pekan_kategori.plot(kind='bar', color='orange', alpha=0.7, label='Hari Libur', ax=ax3)
ax3.set_title('Analisis Pengaruh Cuaca dan Kecepatan Angin terhadap Penggunaan Sepeda (Hari Kerja vs. Hari Libur)')
ax3.set_xlabel('Kondisi Cuaca')
ax3.set_ylabel('Rata-rata Penyewaan')
ax3.legend()
st.pyplot(fig3)

# Insight
st.markdown("""
**Insight:**
- Cerah & Hangat Paling Diminati: Kondisi cuaca "Cerah & Hangat" memiliki rata-rata penyewaan sepeda tertinggi, baik pada hari kerja maupun hari libur.
- Hujan & Dingin Paling Sepi: Kondisi cuaca "Hujan & Dingin" memiliki rata-rata penyewaan sepeda terendah.
- Hari Kerja Sedikit Lebih Tinggi: Rata-rata penyewaan sepeda pada hari kerja sedikit lebih tinggi dibandingkan hari libur di semua kategori kondisi cuaca.
- Pengaruh Konsisten: Pola pengaruh kondisi cuaca terhadap penyewaan sepeda relatif konsisten antara hari kerja dan hari libur.
- Perbedaan Signifikan: Terdapat perbedaan signifikan dalam rata-rata penyewaan antara kondisi cuaca "Cerah & Hangat" dan "Hujan & Dingin".

""")

# --- Analisis Lanjutan: Box Plot Bulanan ---
st.header("Distribusi Penyewaan Sepeda per Bulan")

# Visualisasi
fig4, ax4 = plt.subplots(figsize=(12, 6))
sns.boxplot(x='mnth', y='cnt', data=hour_df, ax=ax4)
ax4.set_title('Distribusi Penyewaan Sepeda per Bulan')
ax4.set_xlabel('Bulan')
ax4.set_ylabel('Jumlah Penyewaan')
ax4.set_xticks(range(12))
ax4.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
st.pyplot(fig4)

# Insight
st.markdown("""
**Insight:**
- Pola Musiman Kuat: Terlihat jelas adanya pola musiman dalam penyewaan sepeda.
- Puncak Musim Panas: Penyewaan tertinggi terjadi pada bulan-bulan musim panas (Juni, Juli, Agustus), dengan median dan kuartil tertinggi.
- Musim Dingin
- Terendah: Penyewaan terendah terjadi pada bulan-bulan musim dingin (Januari, Februari, Desember), dengan median dan kuartil terendah.
- Variasi Tinggi: Variasi penyewaan (rentang antar kuartil dan outlier) cenderung lebih tinggi pada bulan-bulan musim panas.
- Outlier: Terdapat banyak outlier di semua bulan, menunjukkan adanya hari-hari dengan penyewaan yang sangat tinggi atau sangat rendah.
- Tren Meningkat: Ada tren peningkatan penyewaan dari bulan Januari hingga Juni/Juli.
- Tren Menurun: Setelah puncak di musim panas, ada tren penurunan penyewaan hingga bulan Desember.

""")

# Tambahkan bagian copyright dan keterangan
st.markdown("---")
st.markdown(
    """
    *Copyright © 2025 MC172D5X1392 - Richelle Vania Thionanda*

    _Dashboard analisis dan visualisasi data._
    _Kode & visualisasi harap cantumkan sumber._
    """,
    unsafe_allow_html=True
)
