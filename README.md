# Proyek Analisis Data: Bike Sharing Dataset

## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis pola peminjaman sepeda menggunakan Bike Sharing Dataset. Dataset ini berisi data peminjaman sepeda di Washington D.C. selama tahun 2011–2012.

Analisis difokuskan pada pengaruh musim, kondisi cuaca, serta pola penggunaan berdasarkan waktu (jam operasional dan tipe hari). Dataset ini menunjukkan bahwa peminjaman sepeda dipengaruhi oleh faktor lingkungan seperti cuaca, musim, dan waktu penggunaan.

## Pertanyaan Bisnis

1. Bagaimana pengaruh musim dan kondisi cuaca terhadap rata-rata jumlah peminjaman sepeda selama tahun 2011–2012?
2. Bagaimana pola peminjaman sepeda berdasarkan jam operasional, serta bagaimana perbedaannya antara hari kerja dan hari libur selama tahun 2011–2012?

## Insight Utama

* Peminjaman sepeda tertinggi terjadi pada musim Fall dan kondisi cuaca cerah.
* Kondisi cuaca buruk seperti hujan atau salju menurunkan jumlah peminjaman.
* Terdapat pola jam sibuk pada pagi dan sore hari.
* Pada hari kerja, peminjaman lebih tinggi pada jam berangkat dan pulang kerja.

## Struktur Direktori

## 📁 Struktur Direktori
```
submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```
## Setup Environment

### Menggunakan Anaconda

conda create --name bike-sharing python=3.11
conda activate bike-sharing
pip install -r requirements.txt

### Menggunakan Terminal / CMD

pip install -r requirements.txt

## Menjalankan Notebook

jupyter notebook

Kemudian buka file:
notebook.ipynb

## Menjalankan Dashboard (Local)

Jalankan perintah berikut di terminal:

streamlit run dashboard/dashboard.py

Dashboard akan otomatis terbuka di browser.

## Akses Dashboard Online

Link dashboard dapat dilihat pada file:
url.txt

## Library yang Digunakan

* pandas
* numpy
* matplotlib
* seaborn
* streamlit

## Author

* Nama: Keisya Nazalia Azally
