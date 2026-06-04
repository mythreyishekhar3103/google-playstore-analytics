import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/Google-Playstore.csv")

st.title("📊 Category Analysis")

apps = (
    df.groupby("Category")
      .size()
      .reset_index(name="Apps")
      .sort_values("Apps", ascending=False)
      .head(20)
)

fig = px.treemap(
    apps,
    path=["Category"],
    values="Apps",
    title="Category Market Share"
)

st.plotly_chart(fig, use_container_width=True)
