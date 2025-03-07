import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Fungsi untuk menyiapkan berbagai dataframe
def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    }).reset_index()
    daily_rentals_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
    
    return daily_rentals_df

def create_weather_df(df):
    weather_df = df.groupby("weathersit").cnt.sum().reset_index()
    weather_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
    
    return weather_df

def create_weekday_df(df):
    weekday_df = df.groupby("weekday").cnt.sum().reset_index()
    weekday_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
    
    return weekday_df

def create_monthly_rentals_df(df):
    monthly_df = df.groupby("mnth").cnt.sum().reset_index()
    monthly_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
    
    return monthly_df

# Load dataset
bike_df = pd.read_csv(r"C:\Submission\Dashboard\day.csv")

# Konversi tanggal
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])

# Sidebar filter tanggal
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=bike_df["dteday"].min(),
        max_value=bike_df["dteday"].max(),
        value=[bike_df["dteday"].min(), bike_df["dteday"].max()]
    )

# Filter data berdasarkan tanggal yang dipilih
filtered_df = bike_df[(bike_df["dteday"] >= str(start_date)) & 
                      (bike_df["dteday"] <= str(end_date))]

# Persiapan dataframe analisis
daily_rentals_df = create_daily_rentals_df(filtered_df)
weather_df = create_weather_df(filtered_df)
weekday_df = create_weekday_df(filtered_df)
monthly_df = create_monthly_rentals_df(filtered_df)

# Header Dashboard
st.header(" Bike Sharing Dashboard ")

# Statistik utama
col1, col2 = st.columns(2)

with col1:
    total_rentals = daily_rentals_df.total_rentals.sum()
    st.metric("Total Rentals", value=total_rentals)

with col2:
    avg_rentals = round(daily_rentals_df.total_rentals.mean(), 1)
    st.metric("Average Rentals per Day", value=avg_rentals)

# Tren Penyewaan Harian
st.subheader("📈 Daily Rentals Trend")
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(data=daily_rentals_df, x='dteday', y='total_rentals', marker='o', linewidth=2, color="#90CAF9")
ax.set_title("Tren Penyewaan Sepeda Berdasarkan Tanggal")
st.pyplot(fig)

# Pengaruh Cuaca terhadap Penyewaan
st.subheader(" Rentals by Weather Condition")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=weather_df, x='weathersit', y='total_rentals', palette="Blues_r")
ax.set_title("Jumlah Penyewaan Berdasarkan Kondisi Cuaca")
st.pyplot(fig)

# Penyewaan berdasarkan Hari dalam Seminggu
st.subheader("Rentals by Day of the Week")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=weekday_df, x='weekday', y='total_rentals', palette="coolwarm")
ax.set_title("Jumlah Penyewaan Berdasarkan Hari")
st.pyplot(fig)

# Tren Penyewaan Bulanan
st.subheader("Monthly Rentals Trend")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=monthly_df, x='mnth', y='total_rentals', palette="viridis")
ax.set_title("Jumlah Penyewaan Sepeda per Bulan")
st.pyplot(fig)

st.caption(" Selamat Menganalisis! ")  
