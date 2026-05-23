import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="Africa Energy Access Dashboard",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
df = pd.read_excel("african_energy_access.xls")

# =========================
# TITLE
# =========================
st.title("🌍 Energy Access in Africa Dashboard")
st.markdown(
    "### A Decade of Electricity Access Analysis Across African Countries"
)

# =========================
# SIDEBAR FILTERS (SLICERS)
# =========================
st.sidebar.header("🔍 Filter Dashboard")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

# =========================
# FILTER DATA
# =========================
filtered_df = df[
    (df["Region"].isin(selected_region)) &
    (df["Year"].isin(selected_year))
]

# =========================
# KPI CALCULATIONS
# =========================
avg_access = filtered_df["Energy Access (%)"].mean()

highest_access = filtered_df["Energy Access (%)"].max()

lowest_access = filtered_df["Energy Access (%)"].min()

countries_above_80 = filtered_df[
    filtered_df["Energy Access (%)"] >= 80
]["Country"].nunique()

# =========================
# KPI CARDS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Access",
    f"{avg_access:.2f}%"
)

col2.metric(
    "Highest Access",
    f"{highest_access:.2f}%"
)

col3.metric(
    "Lowest Access",
    f"{lowest_access:.2f}%"
)

col4.metric(
    "Countries Above 80%",
    countries_above_80
)

st.markdown("---")

# =========================
# TREND ANALYSIS
# =========================
st.subheader("📈 Energy Access Trend Over Time")

trend_data = (
    filtered_df.groupby("Year")["Energy Access (%)"]
    .mean()
)

st.line_chart(trend_data)

# =========================
# REGION COMPARISON
# =========================
st.subheader("🌍 Regional Comparison")

region_data = (
    filtered_df.groupby("Region")["Energy Access (%)"]
    .mean()
)

st.bar_chart(region_data)

# =========================
# ACCESS CATEGORY DISTRIBUTION
# =========================
st.subheader("📊 Access Category Distribution")

access_category = (
    filtered_df["Access Category"]
    .value_counts()
)

st.bar_chart(access_category)

# =========================
# TOP 10 COUNTRIES
# =========================
st.subheader("🏆 Top 10 Countries by Energy Access")

top10 = (
    filtered_df.groupby("Country")["Energy Access (%)"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top10)

# =========================
# BOTTOM 10 COUNTRIES
# =========================
st.subheader("⚠️ Bottom 10 Countries by Energy Access")

bottom10 = (
    filtered_df.groupby("Country")["Energy Access (%)"]
    .mean()
    .sort_values(ascending=True)
    .head(10)
)

st.bar_chart(bottom10)

# =========================
# DATA PREVIEW
# =========================
st.subheader("📄 Dataset Preview")

st.dataframe(filtered_df)

# =========================
# INSIGHTS SECTION
# =========================
st.subheader("💡 Key Insights")

st.markdown("""
- Energy access improved gradually across many African countries over the decade.
- North African countries generally recorded the highest electricity access rates.
- Several countries in Eastern and Western Africa still experience low access levels.
- Regional disparities remain significant despite steady growth.
- Countries with higher growth rates show stronger infrastructure expansion potential.
""")
