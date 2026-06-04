st.markdown("""
<style>

.main{
background-color:#f5f7fa;
}

[data-testid="metric-container"]{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0px 2px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Google Play Store Analytics",
    page_icon="📱",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/Google-Playstore.csv")

    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Maximum Installs"] = pd.to_numeric(
        df["Maximum Installs"], errors="coerce"
    )

    return df

df = load_data()

st.title("📱 Google Play Store Deep Analytics Dashboard")

st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Select Category",
    df["Category"].dropna().unique()
)

if category:
    df = df[df["Category"].isin(category)]

# KPI CARDS
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Apps", f"{len(df):,}")

col2.metric(
    "Average Rating",
    round(df["Rating"].mean(),2)
)

col3.metric(
    "Total Installs",
    f"{df['Maximum Installs'].sum():,.0f}"
)

col4.metric(
    "Categories",
    df["Category"].nunique()
)

st.divider()

# Top Categories
top_cat = (
    df.groupby("Category")["App Name"]
    .count()
    .sort_values(ascending=False)
    .head(15)
)

fig = px.bar(
    top_cat,
    title="Top Categories by Number of Apps"
)

st.plotly_chart(fig, use_container_width=True)

# Ratings Distribution
fig2 = px.histogram(
    df,
    x="Rating",
    nbins=40,
    title="Ratings Distribution"
)

st.plotly_chart(fig2, use_container_width=True)
