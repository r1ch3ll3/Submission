import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from PIL import Image
import os

# Load dataset
hour_df = pd.read_csv("Data/hour.csv")
day_df = pd.read_csv("Data/day.csv")

# Konversi tanggal
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #B0C4DE; /* Steel Blue */
    }
    [data-testid="stAppViewContainer"]{
        background-color: #B0E0E6; /* Light Powder Blue */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- Sidebar ---
with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])  # Contoh rasio lebar kolom

    with col2:
        logo_path = "Dashboard/bike_sharing_logo.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width=200)
        else:
            st.warning(f"File logo tidak ditemukan di: {logo_path}")

    st.header("Filter Data")
    start_date = st.date_input("Tanggal Mulai", hour_df["dteday"].min())
    end_date = st.date_input("Tanggal Akhir", hour_df["dteday"].max())

    # Filter Musim
    seasons = st.multiselect(
        "Pilih Musim (WAJIB: Pilih Semua)",
        options=["Spring", "Summer", "Fall", "Winter"],
        default=["Spring", "Summer", "Fall", "Winter"]
    )

    if len(seasons) < 4:
        st.error("Analisis memerlukan data dari semua musim. Mohon pilih semua opsi.")
        st.stop() # Stop execution if not all are selected

# Mapping numerik ke nama musim (jika diperlukan)
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
hour_df["season_name"] = hour_df["season"].map(season_map)
day_df["season_name"] = day_df["season"].map(season_map)


# Filter data
# Filter data
if start_date and end_date:
    hour_df = hour_df[
        (hour_df["dteday"] >= pd.to_datetime(start_date))
        & (hour_df["dteday"] <= pd.to_datetime(end_date))
    ]
    day_df = day_df[
        (day_df["dteday"] >= pd.to_datetime(start_date))
        & (day_df["dteday"] <= pd.to_datetime(end_date))
    ]
elif start_date or end_date:
    warning_message = "Mohon masukkan "
    if not start_date:
        warning_message += "Tanggal Mulai"
    if not start_date and not end_date:
        warning_message += " dan "
    if not end_date:
        warning_message += "Tanggal Akhir"
    warning_message += " untuk filter data."
    st.warning(warning_message)
    st.stop()
else:
    st.info("Tidak ada filter tanggal yang diterapkan.")

# Filter musim
hour_df = hour_df[hour_df["season_name"].isin(seasons)]
day_df = day_df[day_df["season_name"].isin(seasons)]


# --- Main Page ---
st.title("Bike Sharing Dashboard")

# --- Statistik Utama ---
st.header("Statistik Utama")
total_rentals = int(hour_df["cnt"].sum())
avg_rentals_day = int(hour_df.groupby("dteday")["cnt"].sum().mean())
avg_rentals_hour = int(hour_df["cnt"].mean())

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", f"{total_rentals:,}")
col2.metric("Rata-rata Penyewaan per Hari", f"{avg_rentals_day:,}")
col3.metric("Rata-rata Penyewaan per Jam", f"{avg_rentals_hour:,}")

# --- Pertanyaan 1: Pengaruh Cuaca ---
st.header("Pengaruh Cuaca terhadap Penyewaan Sepeda")

# Data preparation
cuaca_hari_kerja = hour_df[hour_df['workingday'] == 1].groupby('weathersit')['cnt'].mean()
cuaca_hari_libur = hour_df[hour_df['holiday'] == 0].groupby('weathersit')['cnt'].mean()
cuaca_pengaruh_df = pd.DataFrame({'Hari Kerja': cuaca_hari_kerja, 'Hari Libur': cuaca_hari_libur})
cuaca_pengaruh_df.index = ['Cerah', 'Mendung', 'Hujan Ringan', 'Cuaca Buruk']

# Visualisasi
fig1, ax1 = plt.subplots(figsize=(10, 6))
cuaca_pengaruh_df.plot(kind='bar', ax=ax1, color=['steelblue', 'powderblue']) # Apply colors here
ax1.set_title('Pengaruh Cuaca terhadap Penyewaan Sepeda')
ax1.set_xlabel('Kondisi Cuaca (weathersit)')
ax1.set_ylabel('Rata-rata Penyewaan')
ax1.tick_params(axis='x', rotation=0)
st.pyplot(fig1)

# Insight
st.markdown(
    """
**Insight:**
- Cuaca Cerah Paling Diminati: Kondisi cuaca cerah (Cerah) memiliki rata-rata penyewaan sepeda tertinggi, baik pada hari kerja maupun hari libur.
- Cuaca Buruk Kurangi Penyewaan: Kondisi cuaca buruk (Cuaca Buruk) memiliki rata-rata penyewaan sepeda terendah, baik pada hari kerja maupun hari libur.
- Hari Kerja Sedikit Lebih Tinggi: Rata-rata penyewaan sepeda pada hari kerja sedikit lebih tinggi dibandingkan hari libur di semua kondisi cuaca.
- Pengaruh Cuaca Konsisten: Pola pengaruh cuaca terhadap penyewaan sepeda relatif konsisten antara hari kerja dan hari libur.
- Perbedaan Signifikan: Terdapat perbedaan signifikan dalam rata-rata penyewaan antara kondisi cuaca cerah dan kondisi cuaca buruk.
"""
)

# --- Pertanyaan 2: Tren Bulanan ---
st.header("Tren Penyewaan Sepeda Setiap Bulan")

# Data preparation
monthly_rentals = hour_df.groupby("mnth")["cnt"].sum()

# Visualisasi
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(monthly_rentals.index, monthly_rentals.values, marker="o")
ax2.set_title("Tren Penyewaan Sepeda Setiap Bulan")
ax2.set_xlabel("Bulan")
ax2.set_ylabel("Total Penyewaan")
ax2.set_xticks(range(1, 13))
ax2.set_xticklabels(
    ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
)
ax2.grid(True)
st.pyplot(fig2)

# Insight
st.markdown(
    """
**Insight:**
- Puncak Musim Panas: Jumlah penyewaan sepeda mencapai puncaknya pada bulan-bulan musim panas, khususnya Juni, Juli, dan Agustus.
- Musim Dingin Sepi Peminat: Jumlah penyewaan sepeda terendah terjadi pada bulan-bulan musim dingin, yaitu Januari dan Februari.
- Tren Meningkat Stabil: Terdapat tren peningkatan stabil dalam penyewaan sepeda dari bulan Januari hingga Agustus.
- Tren Menurun Stabil: Setelah puncak di bulan Agustus, terjadi tren penurunan stabil dalam penyewaan sepeda hingga bulan Desember.
- Pola Musiman yang Jelas: Grafik menunjukkan pola musiman yang jelas, dengan fluktuasi signifikan antara bulan-bulan musim panas dan musim dingin.
"""
)

# --- Analisis Lanjutan: Kategori Cuaca ---
st.header(
    "Analisis Pengaruh Cuaca dan Kecepatan Angin terhadap Penggunaan Sepeda (Hari Kerja vs. Hari Libur)"
)


# Fungsi kategori cuaca
def kategori_cuaca(row):
    if row["atemp"] > 0.6 and row["hum"] < 0.4 and row["windspeed"] < 0.3:
        return "Cerah & Hangat"
    elif row["atemp"] < 0.3 and row["hum"] > 0.7 and row["windspeed"] > 0.5:
        return "Hujan & Dingin"
    elif row["atemp"] < 0.5 and row["hum"] > 0.6 and row["windspeed"] < 0.4:
        return "Mendung & Dingin"
    elif row["atemp"] > 0.6 and row["hum"] > 0.6 and row["windspeed"] < 0.3:
        return "Mendung & Hangat"
    else:
        return "Lainnya"


hour_df["kondisi_cuaca"] = hour_df.apply(kategori_cuaca, axis=1)

# Data preparation
cuaca_hari_kerja_kategori = (
    hour_df[hour_df["workingday"] == 1].groupby("kondisi_cuaca")["cnt"].mean()
)
cuaca_akhir_pekan_kategori = (
    hour_df[hour_df["holiday"] == 0].groupby("kondisi_cuaca")["cnt"].mean()
)

# Visualisasi
fig3, ax3 = plt.subplots(figsize=(12, 6))
cuaca_hari_kerja_kategori.plot(kind="bar", color="steelblue", alpha=0.7, label="Hari Kerja", ax=ax3)
cuaca_akhir_pekan_kategori.plot(
    kind="bar", color="powderblue", alpha=0.7, label="Hari Libur", ax=ax3
)
ax3.set_title(
    "Analisis Pengaruh Cuaca dan Kecepatan Angin terhadap Penggunaan Sepeda (Hari Kerja vs. Hari Libur)"
)
ax3.set_xlabel("Kondisi Cuaca")
ax3.set_ylabel("Rata-rata Penyewaan")
ax3.legend()
st.pyplot(fig3)

# Insight
st.markdown(
    """
**Insight:**
- Cerah & Hangat Paling Diminati: Kondisi cuaca "Cerah & Hangat" memiliki rata-rata penyewaan sepeda tertinggi, baik pada hari kerja maupun hari libur.
- Hujan & Dingin Paling Sepi: Kondisi cuaca "Hujan & Dingin" memiliki rata-rata penyewaan sepeda terendah.
- Hari Kerja Sedikit Lebih Tinggi: Rata-rata penyewaan sepeda pada hari kerja sedikit lebih tinggi dibandingkan hari libur di semua kategori kondisi cuaca.
- Pengaruh Konsisten: Pola pengaruh kondisi cuaca terhadap penyewaan sepeda relatif konsisten antara hari kerja dan hari libur.
- Perbedaan Signifikan: Terdapat perbedaan signifikan dalam rata-rata penyewaan antara kondisi cuaca "Cerah & Hangat" dan "Hujan & Dingin".
"""
)

# --- Analisis Lanjutan: Box Plot Bulanan ---
st.header("Distribusi Penyewaan Sepeda per Bulan")

# Visualisasi (Bar Chart)
plt.figure(figsize=(12, 6))
plt.bar(monthly_rentals.index, monthly_rentals.values, color=sns.color_palette('PuBu_r', len(monthly_rentals)))  # Bar chart
plt.title('Total Penyewaan Sepeda per Bulan')  # Judul yang lebih sesuai
plt.xlabel('Bulan')
plt.ylabel('Total Penyewaan')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
plt.show()

# Insight
st.markdown(
    """
**Insight:**
- Pola Musiman Kuat: Terlihat jelas adanya pola musiman dalam penyewaan sepeda.
- Puncak Musim Panas: Penyewaan tertinggi terjadi pada bulan-bulan musim panas (Juni, Juli, Agustus), dengan median dan kuartil tertinggi.
- Musim Dingin Terendah: Penyewaan terendah terjadi pada bulan-bulan musim dingin (Januari, Februari, Desember), dengan median dan kuartil terendah.
- Variasi Tinggi: Variasi penyewaan (rentang antar kuartil dan outlier) cenderung lebih tinggi pada bulan-bulan musim panas.
- Outlier: Terdapat banyak outlier di semua bulan, menunjukkan adanya hari-hari dengan penyewaan yang sangat tinggi atau sangat rendah.
- Tren Meningkat: Ada tren peningkatan penyewaan dari bulan Januari hingga Juni/Juli.
- Tren Menurun: Setelah puncak di musim panas, ada tren penurunan penyewaan hingga bulan Desember.
"""
)

# --- Distribusi Penyewa ---
st.header("Distribusi Penyewa (Casual vs. Registered)")
casual_rentals = hour_df["casual"].sum()
registered_rentals = hour_df["registered"].sum()

fig5, ax5 = plt.subplots(figsize=(8, 8))
colors = ['steelblue', 'powderblue']  # Define the colors
ax5.pie(
    [casual_rentals, registered_rentals],
    labels=["Casual", "Registered"],
    autopct="%1.1f%%",
    startangle=90,
    colors=colors  # Apply the colors
)
ax5.set_title("Distribusi Jenis Penyewa")
st.pyplot(fig5)

st.markdown(
    f"""
**Insight:**
- Penyewa Terdaftar Dominan: Sebanyak {registered_rentals:,} ({registered_rentals / (casual_rentals + registered_rentals) * 100:.1f}%) penyewa adalah pengguna terdaftar, menunjukkan basis pelanggan yang setia.
- Penyewa Casual Signifikan: Namun, penyewa casual juga menyumbang sebesar {casual_rentals:,} ({casual_rentals / (casual_rentals + registered_rentals) * 100:.1f}%), menunjukkan pentingnya menarik dan mempertahankan pengguna sesekali.
"""
)

# --- Pengaruh Jam terhadap Penyewaan ---
st.header("Pengaruh Jam terhadap Penyewaan")

hourly_rentals = hour_df.groupby("hr")["cnt"].mean()

fig6, ax6 = plt.subplots(figsize=(12, 6))
ax6.plot(hourly_rentals.index, hourly_rentals.values, marker="o", color="steelblue")
ax6.set_title("Rata-rata Penyewaan Sepeda per Jam")
ax6.set_xlabel("Jam (0-23)")
ax6.set_ylabel("Rata-rata Penyewaan")
ax6.set_xticks(range(24))
ax6.grid(True)
st.pyplot(fig6)

# Insight
st.markdown(
    """
**Insight:**
- Puncak Pagi dan Sore: Terjadi dua puncak penyewaan, yaitu sekitar jam 8 pagi dan 5-6 sore, yang kemungkinan besar terkait dengan jam berangkat dan pulang kerja.
- Penyewaan Siang Hari Stabil: Penyewaan relatif stabil di siang hari.
- Penyewaan Malam Hari Rendah: Penyewaan terendah terjadi pada malam hari.
"""
)

# --- Kesimpulan Umum ---
st.header("Kesimpulan Umum")

st.markdown(
    """
**Kesimpulan Umum:**

Analisis ini mengungkapkan beberapa pola penting dalam data penyewaan sepeda:

-  **Cuaca:** Kondisi cuaca sangat memengaruhi penyewaan, dengan cuaca cerah dan hangat mendorong lebih banyak penggunaan dan cuaca buruk menghambatnya.
-  **Musim:** Penyewaan memiliki pola musiman yang kuat, dengan puncak pada musim panas dan penurunan pada musim dingin.
-  **Waktu:** Penyewaan bervariasi sepanjang hari, dengan puncak pada jam sibuk perjalanan dan penurunan pada malam hari.
-  **Jenis Pengguna:** Pengguna terdaftar adalah mayoritas, tetapi pengguna casual juga penting.

**Rekomendasi:**

-  **Optimasi Operasional:** Sesuaikan ketersediaan sepeda dan staf berdasarkan pola musiman dan harian.
-  **Strategi Pemasaran:** Targetkan kampanye pemasaran untuk menarik dan mempertahankan pengguna casual. Promosikan penggunaan sepeda pada hari dan jam dengan cuaca baik.
-  **Perencanaan Infrastruktur:** Pertimbangkan rute dan fasilitas yang mendukung penggunaan sepeda untuk komuter.
"""
)

# Tambahkan bagian copyright dan keterangan
st.markdown("---")
st.markdown(
    """
    *Copyright © 2025 MC172D5X1392 - Richelle Vania Thionanda*

    _Dashboard analisis dan visualisasi data._
    _Kode & visualisasi harap cantumkan sumber._
    """,
    unsafe_allow_html=True,
)
