import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Google Play Store Analytics",
    page_icon="📱",
    layout="wide"
)

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


@st.cache_data
def load_data():
    df = pd.read_csv("data/googleplaystore.csv")

    # Clean column names
    df.columns = df.columns.str.strip()

    if "Rating" in df.columns:
        df["Rating"] = pd.to_numeric(
            df["Rating"],
            errors="coerce"
        )

    # Handle installs column
    installs_col = None

    possible_cols = [
        "Maximum Installs",
        "Installs",
        "Maximum_Installs"
    ]

    for col in possible_cols:
        if col in df.columns:
            installs_col = col
            break

    if installs_col:
        df[installs_col] = (
            df[installs_col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("+", "", regex=False)
        )

        df[installs_col] = pd.to_numeric(
            df[installs_col],
            errors="coerce"
        )

    return df, installs_col


df, installs_col = load_data()

st.title("📱 Google Play Store Deep Analytics Dashboard")

st.sidebar.header("Filters")

if "Category" in df.columns:

    category = st.sidebar.multiselect(
        "Select Category",
        sorted(df["Category"].dropna().unique())
    )

    if category:
        df = df[df["Category"].isin(category)]

# KPI SECTION

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Apps",
    f"{len(df):,}"
)

if "Rating" in df.columns:
    avg_rating = round(df["Rating"].mean(), 2)
else:
    avg_rating = 0

col2.metric(
    "Average Rating",
    avg_rating
)

if installs_col:
    total_installs = int(df[installs_col].sum())
else:
    total_installs = 0

col3.metric(
    "Total Installs",
    f"{total_installs:,}"
)

if "Category" in df.columns:
    categories = df["Category"].nunique()
else:
    categories = 0

col4.metric(
    "Categories",
    categories
)

st.divider()

# CATEGORY ANALYSIS

if "Category" in df.columns and "App Name" in df.columns:

    top_cat = (
        df.groupby("Category")["App Name"]
        .count()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        top_cat,
        x="Category",
        y="App Name",
        title="Top Categories by Number of Apps"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# RATINGS DISTRIBUTION

if "Rating" in df.columns:

    fig2 = px.histogram(
        df,
        x="Rating",
        nbins=40,
        title="Ratings Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# INSTALLS ANALYSIS

if installs_col and "Category" in df.columns:

    installs_by_cat = (
        df.groupby("Category")[installs_col]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig3 = px.bar(
        installs_by_cat,
        x="Category",
        y=installs_col,
        title="Top Categories by Installs"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# DEBUG SECTION

with st.expander("Dataset Columns"):
    st.write(df.columns.tolist())
