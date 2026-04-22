import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =====================================
# CONFIG PAGE
# =====================================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

sns.set_style("whitegrid")

st.title("🚲 Bike Sharing Dashboard")
st.markdown("Dashboard interaktif analisis data penyewaan sepeda.")

# =====================================
# LOAD DATA
# =====================================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)

    day_path = os.path.join(base_dir, "day.csv")
    hour_path = os.path.join(base_dir, "hour.csv")

    day_df = pd.read_csv(day_path)
    hour_df = pd.read_csv(hour_path)

    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

    return day_df, hour_df

day_df, hour_df = load_data()

# =====================================
# MAPPING
# =====================================
season_map = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

weather_map = {
    1: "Clear",
    2: "Mist / Cloudy",
    3: "Light Rain / Snow"
}

day_df["season_label"] = day_df["season"].map(season_map)
day_df["weather_label"] = day_df["weathersit"].map(weather_map)

# =====================================
# SIDEBAR
# =====================================
st.sidebar.header("📌 Filter Data")

year_option = st.sidebar.selectbox(
    "Pilih Tahun",
    ["Semua", 2011, 2012]
)

season_option = st.sidebar.selectbox(
    "Pilih Musim",
    ["Semua", "Spring", "Summer", "Fall", "Winter"]
)

# =====================================
# FILTER
# =====================================
filtered_df = day_df.copy()

if year_option != "Semua":
    yr_val = 0 if year_option == 2011 else 1
    filtered_df = filtered_df[filtered_df["yr"] == yr_val]

if season_option != "Semua":
    filtered_df = filtered_df[
        filtered_df["season_label"] == season_option
    ]

# =====================================
# KPI
# =====================================
st.subheader("📈 Ringkasan")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rental", f"{filtered_df['cnt'].sum():,.0f}")
col2.metric("Rata-rata Harian", f"{filtered_df['cnt'].mean():,.0f}")
col3.metric("Rental Tertinggi", f"{filtered_df['cnt'].max():,.0f}")

# =====================================
# ROW 1
# =====================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Rental Berdasarkan Musim")

    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(
        data=filtered_df,
        x="season_label",
        y="cnt",
        palette="viridis",
        ax=ax
    )
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Rental")
    st.pyplot(fig)

with col2:
    st.subheader("🌤️ Rental Berdasarkan Cuaca")

    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(
        data=filtered_df,
        x="weather_label",
        y="cnt",
        palette="coolwarm",
        ax=ax
    )
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Jumlah Rental")
    st.pyplot(fig)

# =====================================
# ROW 2
# =====================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("⏰ Rata-rata Rental per Jam")

    hourly = hour_df.groupby("hr")["cnt"].mean()

    fig, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(
        x=hourly.index,
        y=hourly.values,
        marker="o",
        linewidth=3,
        color="green",
        ax=ax
    )
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rental")
    st.pyplot(fig)

with col2:
    st.subheader("🏢 Hari Kerja vs Hari Libur")

    fig, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(
        data=hour_df,
        x="hr",
        y="cnt",
        hue="workingday",
        palette=["orange", "blue"],
        linewidth=3,
        ax=ax
    )
    ax.legend(["Libur", "Hari Kerja"])
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rental")
    st.pyplot(fig)

# =====================================
# ROW 3
# =====================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Tren Rental Bulanan")

    monthly = day_df.groupby("mnth")["cnt"].mean()

    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(
        x=monthly.index,
        y=monthly.values,
        palette="magma",
        ax=ax
    )
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Rental")
    st.pyplot(fig)

with col2:
    st.subheader("👥 Casual vs Registered")

    users = day_df[["casual", "registered"]].sum()

    fig, ax = plt.subplots(figsize=(8,5))
    ax.pie(
        users,
        labels=users.index,
        autopct="%1.1f%%",
        colors=["skyblue", "lightgreen"],
        startangle=90
    )
    st.pyplot(fig)

# =====================================
# INSIGHT
# =====================================
st.subheader("📌 Insight Utama")

st.markdown("""
✅ Pengguna **registered** mendominasi penyewaan sepeda  
✅ Peak hour terjadi pukul **08.00** dan **17.00 - 18.00**  
✅ Musim **Fall** memiliki jumlah rental tertinggi  
✅ Cuaca cerah mendorong peningkatan penyewaan  
✅ Bike sharing banyak digunakan sebagai sarana transportasi kerja
""")