# E-Commerce Data Analysis Project

Proyek ini merupakan analisis data dari dataset **Olist E-Commerce** untuk mengeksplorasi pola perilaku pelanggan, loyalitas, serta dampak logistik terhadap kepuasan pelanggan. Hasil analisis ini juga disajikan dalam bentuk dashboard interaktif menggunakan Streamlit.

## Pertanyaan Bisnis
1. Negara bagian (state) dan kota mana yang memiliki konsentrasi pelanggan tertinggi?
2. Berapa banyak pelanggan yang melakukan pembelian lebih dari satu kali (Repeat Order) dan kota mana yang memiliki jumlah repeat buyers terbanyak?
3. Apakah durasi pengiriman yang lama berpengaruh terhadap skor review yang rendah di negara bagian tertentu?

## Struktur Folder
- `/data`: Berisi dataset mentah (CSV).
- `submission.ipynb`: File analisis data lengkap mulai dari Wrangling hingga Visualization.
- `dashboard.py`: File utama untuk menjalankan dashboard Streamlit.
- `all_data.csv`: Dataset yang telah dibersihkan untuk digunakan oleh dashboard.
- `requirements.txt`: Daftar library Python yang dibutuhkan.

## Cara Menjalankan Dashboard

### 1. Persiapan Lingkungan (Environment)
Pastikan Anda memiliki Python terinstal. Disarankan menggunakan *virtual environment*.

```bash
conda create --name olist-ds python=3.9
conda activate olist-ds
pip install -r requirements.txt# olist-data-analysis
