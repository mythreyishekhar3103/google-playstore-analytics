import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Category Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Category Analysis")

# Load Dataset
try:
    df = pd.read_csv("data/googleplaystore.csv")
except FileNotFoundError:
    st.error(
        "Dataset not found. Make sure googleplaystore.csv is inside the data folder."
    )
    st.stop()

# Clean column names
df.columns = df.columns.str.strip()

# Check Category column
if "Category" not in df.columns:
    st.error("Category column not found in dataset.")
    st.write("Available Columns:")
    st.write(df.columns.tolist())
    st.stop()

# Category statistics
apps = (
    df.groupby("Category")
      .size()
      .reset_index(name="Apps")
      .sort_values(
          by="Apps",
          ascending=False
      )
      .head(20)
)

# Metrics
col1, col2 = st.columns(2)

col1.metric(
    "Total Categories",
    df["Category"].nunique()
)

col2.metric(
    "Total Apps",
    len(df)
)

# Treemap
fig = px.treemap(
    apps,
    path=["Category"],
    values="Apps",
    title="Category Market Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Bar Chart
fig2 = px.bar(
    apps,
    x="Category",
    y="Apps",
    title="Top Categories by App Count",
    text="Apps"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# Data Table
st.subheader("Category Statistics")

st.dataframe(
    apps,
    use_container_width=True
)
