import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

@st.cache_data
def load_data():
    day_df = pd.read_csv(DATA_DIR / "day.csv")
    hour_df = pd.read_csv(DATA_DIR / "hour.csv")

    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_map = {
        1: "Clear",
        2: "Mist/Cloudy",
        3: "Light Rain/Snow",
        4: "Heavy Rain/Snow"
    }
    weekday_map = {
        0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
        4: "Thursday", 5: "Friday", 6: "Saturday"
    }

    for df in [day_df, hour_df]:
        df["season"] = df["season"].map(season_map)
        df["weathersit"] = df["weathersit"].map(weather_map)
        df["weekday"] = df["weekday"].map(weekday_map)
        df["year"] = df["yr"].map({0: 2011, 1: 2012})
        df["day_status"] = df["workingday"].map({0: "Hari Libur", 1: "Hari Kerja"})

    return day_df, hour_df


def create_bar_chart(data, x_col, y_col, title, x_label, y_label, order=None, rotation=0):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=data, x=x_col, y=y_col, order=order, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.tick_params(axis="x", rotation=rotation)
    st.pyplot(fig)
    plt.close(fig)


def create_line_chart(data, x_col, y_col, title, x_label, y_label, hue=None):
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=data, x=x_col, y=y_col, hue=hue, marker="o", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if x_col == "hr":
        ax.set_xticks(range(24))
    st.pyplot(fig)
    plt.close(fig)


def create_user_bar(casual_value, registered_value):
    user_df = pd.DataFrame({
        "Tipe Pengguna": ["Casual", "Registered"],
        "Rata-rata": [casual_value, registered_value]
    })
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=user_df, x="Tipe Pengguna", y="Rata-rata", ax=ax)
    ax.set_title("Rata-rata Pengguna Casual vs Registered")
    ax.set_xlabel("Tipe Pengguna")
    ax.set_ylabel("Rata-rata Jumlah Pengguna")
    st.pyplot(fig)
    plt.close(fig)


def create_weekday_chart(data):
    order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=data, x="weekday", y="cnt", order=order, ax=ax)
    ax.set_title("Rata-rata Peminjaman Berdasarkan Hari")
    ax.set_xlabel("Hari")
    ax.set_ylabel("Rata-rata Peminjaman")
    ax.tick_params(axis="x", rotation=20)
    st.pyplot(fig)
    plt.close(fig)


# Main app

day_df, hour_df = load_data()

st.title("Dashboard Analisis Bike Sharing Dataset")
st.markdown(
    "Dashboard ini menampilkan pola peminjaman sepeda berdasarkan **musim**, "
    "**kondisi cuaca**, **hari**, dan **jam operasional**."
)

# Sidebar filters
st.sidebar.header("Filter Data")

season_options = [s for s in ["Spring", "Summer", "Fall", "Winter"] if s in day_df["season"].dropna().unique().tolist()]
weather_options = [
    w for w in ["Clear", "Mist/Cloudy", "Light Rain/Snow", "Heavy Rain/Snow"]
    if w in day_df["weathersit"].dropna().unique().tolist()
]
year_options = sorted(day_df["year"].dropna().unique().tolist())
day_status_options = ["Hari Kerja", "Hari Libur"]

selected_season = st.sidebar.multiselect("Pilih Musim", season_options, default=season_options)
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", weather_options, default=weather_options)
selected_year = st.sidebar.multiselect("Pilih Tahun", year_options, default=year_options)
selected_day_status = st.sidebar.multiselect("Pilih Tipe Hari", day_status_options, default=day_status_options)

filtered_day = day_df[
    day_df["season"].isin(selected_season)
    & day_df["weathersit"].isin(selected_weather)
    & day_df["year"].isin(selected_year)
    & day_df["day_status"].isin(selected_day_status)
].copy()

filtered_hour = hour_df[
    hour_df["season"].isin(selected_season)
    & hour_df["weathersit"].isin(selected_weather)
    & hour_df["year"].isin(selected_year)
    & hour_df["day_status"].isin(selected_day_status)
].copy()

if filtered_day.empty or filtered_hour.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
    st.stop()

# Metrics
st.subheader("Ringkasan Utama")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Peminjaman", f"{int(filtered_day['cnt'].sum()):,}")
col2.metric("Rata-rata Harian", f"{filtered_day['cnt'].mean():.2f}")
col3.metric("Peminjaman Maksimum", f"{int(filtered_day['cnt'].max()):,}")
most_popular_season = filtered_day.groupby("season")["cnt"].mean().sort_values(ascending=False).index[0]
col4.metric("Musim Terpopuler", most_popular_season)

st.markdown("---")

# Row 1
col_a, col_b = st.columns(2)
with col_a:
    season_summary = filtered_day.groupby("season", as_index=False)["cnt"].mean()
    create_bar_chart(
        season_summary,
        x_col="season",
        y_col="cnt",
        title="Rata-rata Peminjaman Berdasarkan Musim",
        x_label="Musim",
        y_label="Rata-rata Peminjaman",
        order=season_options
    )
    st.caption("Musim Fall cenderung memiliki rata-rata peminjaman paling tinggi.")

with col_b:
    weather_summary = filtered_day.groupby("weathersit", as_index=False)["cnt"].mean()
    create_bar_chart(
        weather_summary,
        x_col="weathersit",
        y_col="cnt",
        title="Rata-rata Peminjaman Berdasarkan Kondisi Cuaca",
        x_label="Kondisi Cuaca",
        y_label="Rata-rata Peminjaman",
        order=weather_options,
        rotation=15
    )
    st.caption("Cuaca cerah mendorong peminjaman lebih tinggi dibanding cuaca buruk.")

# Row 2
col_c, col_d = st.columns(2)
with col_c:
    hourly_summary = filtered_hour.groupby("hr", as_index=False)["cnt"].mean()
    create_line_chart(
        hourly_summary,
        x_col="hr",
        y_col="cnt",
        title="Pola Rata-rata Peminjaman Sepeda per Jam",
        x_label="Jam",
        y_label="Rata-rata Peminjaman"
    )
    st.caption("Puncak peminjaman terlihat pada pagi dan sore hari.")

with col_d:
    workingday_summary = filtered_hour.groupby(["day_status", "hr"], as_index=False)["cnt"].mean()
    create_line_chart(
        workingday_summary,
        x_col="hr",
        y_col="cnt",
        hue="day_status",
        title="Perbandingan Hari Kerja dan Hari Libur",
        x_label="Jam",
        y_label="Rata-rata Peminjaman"
    )
    st.caption("Hari kerja menunjukkan lonjakan yang lebih tajam pada jam berangkat dan pulang kerja.")

st.markdown("---")

# Row 3
st.subheader("Karakteristik Pengguna dan Hari")
col_e, col_f = st.columns(2)
with col_e:
    create_user_bar(filtered_day["casual"].mean(), filtered_day["registered"].mean())
    st.caption("Pengguna registered jauh lebih dominan dibanding pengguna casual.")

with col_f:
    weekday_summary = filtered_day.groupby("weekday", as_index=False)["cnt"].mean()
    create_weekday_chart(weekday_summary)
    st.caption("Rata-rata peminjaman berubah menurut hari, mengikuti pola mobilitas mingguan.")

st.markdown("---")

# Insights
st.subheader("Ringkasan Insight")
st.markdown(
    "- Peminjaman sepeda cenderung lebih tinggi pada **musim Fall** dan saat **cuaca cerah**.\n"
    "- Terdapat **jam sibuk** pada pagi dan sore hari, yang menunjukkan pola penggunaan untuk mobilitas harian.\n"
    "- Pada **hari kerja**, intensitas peminjaman umumnya lebih tinggi pada jam berangkat dan pulang kerja.\n"
    "- Pengguna **registered** mendominasi penggunaan layanan dibanding pengguna casual."
)

st.subheader("Kesimpulan")
st.write(
    "Pola peminjaman sepeda dipengaruhi oleh faktor waktu dan lingkungan. "
    "Musim, kondisi cuaca, tipe hari, serta jam operasional memiliki peran penting "
    "dalam menentukan tingkat penggunaan layanan bike sharing."
)
