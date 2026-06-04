import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/Google-Playstore.csv")

st.title("⭐ Rating Analysis")

avg_rating = (
    df.groupby("Category")["Rating"]
    .mean()
    .sort_values(ascending=False)
    .head(20)
)

fig = px.bar(
    avg_rating,
    title="Highest Rated Categories"
)

st.plotly_chart(fig, use_container_width=True)
