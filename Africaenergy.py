import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Africa Energy Access Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================
data = pd.read_excel("african_energy_access.xls")

# ==========================================
# DASHBOARD TITLE
# ==========================================
st.markdown(
    """
    <h1 style='text-align: center; color: #0B3D91;'>
    🌍 Africa Energy Access Dashboard
    </h1>
    <h4 style='text-align: center; color: gray;'>
    A Decade of Electricity Access Analysis Across African Countries
    </h4>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ==========================================
# SIDEBAR FILTERS
# ==========================================
st.sidebar.header("🔍 Dashboard Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=sorted(data["Region"].unique()),
    default=sorted(data["Region"].unique())
)

selected_year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(data["Year"].unique()),
    default=sorted(data["Year"].unique())
)

# ==========================================
# FILTER DATA
# ==========================================
filtered_data = data[
    (data["Region"].isin(selected_region)) &
    (data["Year"].isin(selected_year))
]

# ==========================================
# KPI CALCULATIONS
# ==========================================
avg_access = filtered_data["Energy Access (%)"].mean()

highest_access = filtered_data["Energy Access (%)"].max()

lowest_access = filtered_data["Energy Access (%)"].min()

countries_above_80 = filtered_data[
    filtered_data["Energy Access (%)"] >= 80
]["Country"].nunique()

# ==========================================
# KPI CARDS
# ==========================================
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

# ==========================================
# TREND LINE CHART
# ==========================================
st.subheader("📈 Energy Access Trend Over Time")

trend_data = (
    filtered_data.groupby("Year")["Energy Access (%)"]
    .mean()
    .reset_index()
)

fig_trend = px.line(
    trend_data,
    x="Year",
    y="Energy Access (%)",
    markers=True,
    line_shape="spline",
    color_discrete_sequence=["#0B3D91"]
)

fig_trend.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    title_x=0.3
)

st.plotly_chart(fig_trend, use_container_width=True)

# ==========================================
# REGION COMPARISON BAR CHART
# ==========================================
st.subheader("🌍 Regional Comparison")

region_data = (
    filtered_data.groupby("Region")["Energy Access (%)"]
    .mean()
    .reset_index()
    .sort_values(by="Energy Access (%)", ascending=False)
)

fig_region = px.bar(
    region_data,
    x="Region",
    y="Energy Access (%)",
    text_auto=".2f",
    color="Region",
    color_discrete_sequence=[
        "#0B3D91",
        "#00A896",
        "#F4A261",
        "#E63946"
    ]
)

fig_region.update_traces(
    textposition="outside"
)

fig_region.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    yaxis_title="Average Access (%)"
)

st.plotly_chart(fig_region, use_container_width=True)

# ==========================================
# ACCESS CATEGORY PIE CHART
# ==========================================
st.subheader("🥧 Access Category Distribution")

category_data = (
    filtered_data.groupby("Access Category")["Country"]
    .nunique()
    .reset_index()
)

fig_pie = px.pie(
    category_data,
    names="Access Category",
    values="Country",
    hole=0.4,
    color_discrete_sequence=[
        "#0B3D91",
        "#00A896",
        "#F4A261",
        "#E63946"
    ]
)

fig_pie.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# TOP 10 COUNTRIES
# ==========================================
st.subheader("🏆 Top 10 Countries by Energy Access")

top10 = (
    filtered_data.groupby("Country")["Energy Access (%)"]
    .mean()
    .reset_index()
    .sort_values(by="Energy Access (%)", ascending=False)
    .head(10)
)

fig_top10 = px.bar(
    top10,
    x="Country",
    y="Energy Access (%)",
    text_auto=".2f",
    color="Energy Access (%)",
    color_continuous_scale="Blues"
)

fig_top10.update_traces(
    textposition="outside"
)

fig_top10.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig_top10, use_container_width=True)

# ==========================================
# BOTTOM 10 COUNTRIES
# ==========================================
st.subheader("⚠️ Bottom 10 Countries by Energy Access")

bottom10 = (
    filtered_data.groupby("Country")["Energy Access (%)"]
    .mean()
    .reset_index()
    .sort_values(by="Energy Access (%)", ascending=True)
    .head(10)
)

fig_bottom10 = px.bar(
    bottom10,
    x="Country",
    y="Energy Access (%)",
    text_auto=".2f",
    color="Energy Access (%)",
    color_continuous_scale="Reds"
)

fig_bottom10.update_traces(
    textposition="outside"
)

fig_bottom10.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig_bottom10, use_container_width=True)

# ==========================================
# GROWTH STATUS CHART
# ==========================================
st.subheader("📊 Growth Status Distribution")

growth_data = (
    filtered_data.groupby("Growth Status")["Country"]
    .nunique()
    .reset_index()
)

fig_growth = px.bar(
    growth_data,
    x="Growth Status",
    y="Country",
    text_auto=True,
    color="Growth Status",
    color_discrete_sequence=[
        "#00A896",
        "#F4A261"
    ]
)

fig_growth.update_traces(
    textposition="outside"
)

fig_growth.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    yaxis_title="Number of Countries"
)

st.plotly_chart(fig_growth, use_container_width=True)

# ==========================================
# DATA PREVIEW
# ==========================================
st.subheader("📄 Dataset Preview")

st.dataframe(filtered_data)

# ==========================================
# KEY INSIGHTS
# ==========================================
st.subheader("💡 Key Insights")

st.markdown("""
✅ North African countries consistently recorded the highest electricity access rates.

✅ Significant regional disparities still exist across Africa despite overall growth.

✅ Several Eastern and Western African countries remain below the continental average.

✅ The number of countries with access above 80% increased steadily over the decade.

✅ Southern Africa showed relatively stable and high-performing electricity access trends.

✅ Countries classified under low access categories remain critical targets for infrastructure investment and policy intervention.
""")
