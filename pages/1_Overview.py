import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 Google Play Store Overview")

df = pd.read_csv("data/Google-Playstore.csv")

col1, col2, col3 = st.columns(3)

col1.metric("Total Apps", f"{len(df):,}")

col2.metric(
    "Categories",
    df["Category"].nunique()
)

col3.metric(
    "Average Rating",
    round(df["Rating"].mean(), 2)
)

st.subheader("Top 10 Categories")

top_cat = (
    df["Category"]
    .value_counts()
    .head(10)
)

fig = px.bar(
    top_cat,
    x=top_cat.index,
    y=top_cat.values,
    title="Top Categories"
)

st.plotly_chart(fig, use_container_width=True)
