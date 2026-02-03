import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set konfigurasi halaman
st.set_page_config(page_title="E-Commerce Data Analysis Dashboard", layout="wide")

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    # Pastikan kolom datetime diubah tipenya
    datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
    for col in datetime_columns:
        df[col] = pd.to_datetime(df[col])
    return df

all_df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("Projek Analisis Data")
    st.markdown("### Nama: Naura Fathiahaq Nabila")
    st.markdown("Dataset: Olist E-Commerce")

# --- HEADER ---
st.title("🛒 E-Commerce Public Data Analysis Dashboard")
st.markdown("Dashboard ini menampilkan wawasan utama dari performa penjualan dan kepuasan pelanggan.")

# --- TABS UNTUK RUMUSAN MASALAH ---
tab1, tab2, tab3 = st.tabs(["Geografi Pelanggan", "Loyalitas Pelanggan", "Analisis Pengiriman"])

# --- TAB 1: GEOGRAFI ---
with tab1:
    st.header("📍 Konsentrasi Pelanggan Berdasarkan Wilayah")
    col1, col2 = st.columns(2)

    with col1:
        state_df = all_df.groupby("customer_state").customer_id.nunique().reset_index()
        state_df.columns = ["state", "customer_count"]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(x="customer_count", y="state", data=state_df.sort_values("customer_count", ascending=False), palette="viridis")
        ax.set_title("Jumlah Pelanggan per Negara Bagian")
        st.pyplot(fig)

    with col2:
        st.write("### Insight Utama")
        st.write("""
        - Wilayah **São Paulo (SP)** mendominasi pasar dengan jumlah pelanggan tertinggi.
        - Konsentrasi pelanggan terbesar berada di wilayah **Tenggara (Southeast)** Brazil.
        """)

# --- TAB 2: REPEAT ORDER ---
with tab2:
    st.header("🔁 Analisis Loyalitas Pelanggan")
    
    user_order_counts = all_df.groupby('customer_unique_id').order_id.nunique().reset_index()
    one_time = user_order_counts[user_order_counts['order_id'] == 1].shape[0]
    repeat = user_order_counts[user_order_counts['order_id'] > 1].shape[0]

    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig, ax = plt.subplots()
        ax.pie([one_time, repeat], labels=['Sekali Beli', 'Repeat Order'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

    with col2:
        st.metric("Total Unique Customers", f"{user_order_counts.shape[0]:,}")
        st.metric("Repeat Buyers", f"{repeat:,}")
        st.write("**Kesimpulan:** Mayoritas pelanggan hanya berbelanja satu kali. Diperlukan strategi retensi yang lebih kuat.")

# --- TAB 3: PENGIRIMAN VS REVIEW ---
with tab3:
    st.header("🚚 Dampak Waktu Pengiriman terhadap Rating")
    
    # Menyiapkan data korelasi per state
    state_perf = all_df.groupby('customer_state').agg({
        'delivery_time': 'mean',
        'review_score': 'mean'
    }).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(data=state_perf, x='delivery_time', y='review_score', color='red', ax=ax)
    sns.scatterplot(data=state_perf, x='delivery_time', y='review_score', hue='customer_state', s=100, ax=ax)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)
    
    st.info("💡 **Insight:** Garis regresi menunjukkan tren negatif. Semakin lama waktu pengiriman, semakin rendah skor kepuasan pelanggan.")

st.caption('Copyright (C) 2026 - Naura Fathiahaq Nabila')