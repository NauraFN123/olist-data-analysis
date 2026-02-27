import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Brazilian E-Commerce Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

all_df = load_data()

# Pengaturan sidebar dan filter tanggal
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("Naura's Dashboard")
    
    min_date = all_df["order_purchase_timestamp"].min()
    max_date = all_df["order_purchase_timestamp"].max()

    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data utama berdasarkan input tanggal
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

st.title("Brazilian E-Commerce Analysis Dashboard")
st.markdown(f"Data periode: **{start_date}** sampai **{end_date}**")

# Analisis sebaran pelanggan per negara bagian
st.header("Sebaran Pelanggan Terbesar")
col1, col2 = st.columns([2, 1])

with col1:
    state_cust = main_df.groupby("customer_state").customer_unique_id.nunique().sort_values(ascending=False).reset_index().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="customer_unique_id", y="customer_state", data=state_cust, palette="viridis", ax=ax)
    ax.set_title("10 Negara Bagian dengan Pelanggan Unik Terbanyak")
    st.pyplot(fig)

with col2:
    st.write("### Insight")
    top_state = state_cust.iloc[0]
    st.info(f"Negara bagian {top_state['customer_state']} mendominasi dengan total {top_state['customer_unique_id']:,} pelanggan unik.")

# Analisis tren pesanan tiap kuartal
st.header("Tren Pesanan per Kuartal")
main_df['order_quarter'] = main_df['order_purchase_timestamp'].dt.to_period('Q').astype(str)
quarterly_data = main_df.groupby('order_quarter').order_id.nunique().reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 5))
sns.lineplot(data=quarterly_data, x='order_quarter', y='order_id', marker='o', linewidth=3, ax=ax2)
plt.xticks(rotation=45)
ax2.set_title("Tren Jumlah Pesanan per Kuartal")
st.pyplot(fig2)

# Bagian Analisis Pengiriman di dashboard.py
st.header("Bagaimana Pengiriman Mempengaruhi Kepuasan?")

state_perf = main_df.groupby('customer_state').agg({
    'delivery_time': 'mean',
    'review_score': 'mean'
}).reset_index()

col_a, col_b = st.columns([2, 1])

with col_a:
    fig, ax = plt.subplots(figsize=(10, 6))
    # Menggunakan Regression Plot untuk menunjukkan korelasi (Bagaimana hubungan keduanya)
    sns.regplot(data=state_perf, x='delivery_time', y='review_score', color='red', ax=ax)
    ax.set_title("Hubungan Durasi Pengiriman vs Skor Review")
    st.pyplot(fig)

with col_b:
    correlation = state_perf['delivery_time'].corr(state_perf['review_score'])
    st.metric("Tingkat Korelasi", f"{correlation:.2f}")
    st.write("Insight: Nilai negatif menunjukkan bahwa durasi pengiriman yang lebih lama berakibat pada penurunan skor kepuasan.")

st.caption('Copyright (C) 2026 - Naura Fathiahaq Nabila')