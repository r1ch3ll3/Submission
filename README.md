# 🚴‍♂️ Bike Sharing Dashboard dengan Streamlit  

Dashboard ini dikembangkan menggunakan **Streamlit**, **Pandas**, **Matplotlib**, dan **Seaborn** untuk menganalisis data penyewaan sepeda berdasarkan berbagai faktor seperti tanggal, kondisi cuaca, hari dalam seminggu, dan bulan.  

## 📌 **Persyaratan**  
Sebelum menjalankan proyek ini, pastikan Anda telah menginstal semua pustaka yang diperlukan. 
✅ **Python**   
✅ **Pandas**  
✅ **Matplotlib** 
✅ **Streamlit** 
✅ **Seaborn**  
✅ **Babel**

### 1️⃣ **Instalasi Library yang Dibutuhkan**  
Gunakan perintah berikut untuk menginstal pustaka yang diperlukan:  
```bash
pip install numpy pandas scipy matplotlib seaborn jupyter
```
```bash
pip install streamlit
```
```bash
pip install babel
```

### 2️⃣ **Struktur Direktori**  
Pastikan struktur direktori proyek seperti berikut:  
```
📂 Bike-Sharing-Dashboard
 ┣ 📜 app.py
 ┣ 📜 requirements.txt
 ┣ 📂 data
 ┃ ┗ 📜 day.csv
   ┗ 📜 hour.csv
 ┣ 📜 Notebook.ipynb
 ┣ 📜 README.md
 ┣ 📜 requirement.txt
```
- `app.py` → File utama untuk menjalankan dashboard.  
- `day.csv` → Dataset yang berisi data penyewaan sepeda harian.  
- `README.md` → Panduan penggunaan.  

### 3️⃣ **Menjalankan Dashboard**  
Gunakan perintah berikut untuk menjalankan aplikasi **Streamlit**:  
```bash
streamlit run app.py
```
Setelah itu, **dashboard akan terbuka di browser secara otomatis**.  

## 📊 **Fitur Dashboard**  
1️⃣ **Filter Rentang Waktu** → Memungkinkan pengguna memilih periode waktu yang ingin dianalisis.  
2️⃣ **Statistik Utama** → Menampilkan total penyewaan & rata-rata penyewaan per hari.  
3️⃣ **Grafik Tren Harian** → Menampilkan jumlah penyewaan sepeda berdasarkan tanggal.  
4️⃣ **Analisis Cuaca** → Menunjukkan pengaruh kondisi cuaca terhadap jumlah penyewaan.  
5️⃣ **Analisis Hari dalam Seminggu** → Menampilkan pola penyewaan berdasarkan hari.  
6️⃣ **Analisis Bulanan** → Melihat tren penyewaan berdasarkan bulan.  

## 📁 **Dataset**  
Dataset yang digunakan adalah `day.csv`, yang berisi beberapa kolom penting seperti:  
- `dteday` → Tanggal transaksi penyewaan.  
- `cnt` → Jumlah total penyewaan sepeda.  
- `weathersit` → Kondisi cuaca (1 = Cerah, 2 = Berawan, 3 = Hujan).  
- `weekday` → Hari dalam seminggu (0 = Minggu, 1 = Senin, dst.).  
- `mnth` → Bulan dalam tahun (1 = Januari, 12 = Desember).  

---

💡 **Selamat menganalisis data penyewaan sepeda! 🚴‍♂️📊**  

---
