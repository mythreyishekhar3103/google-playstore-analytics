import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/googleplaystore.csv")

st.title("👨‍💻 Developer Insights")

developers = (
    df.groupby("Developer Id")
    .size()
    .sort_values(ascending=False)
    .head(20)
)

fig = px.bar(
    developers,
    title="Top Developers by App Count"
)

st.plotly_chart(fig, use_container_width=True)
