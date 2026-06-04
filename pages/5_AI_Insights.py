import streamlit as st
import pandas as pd

df = pd.read_csv("data/Google-Playstore.csv")

st.title("🤖 Smart Insights")

highest = df.loc[
    df["Maximum Installs"].idxmax()
]

st.success(
f"""
Most Installed App:
{highest['App Name']}

Category:
{highest['Category']}

Installs:
{highest['Maximum Installs']:,}
"""
)

top_category = (
    df["Category"]
    .value_counts()
    .idxmax()
)

st.info(
f"Most Popular Category: {top_category}"
)

avg_rating = round(
    df["Rating"].mean(),
    2
)

st.warning(
f"Average Play Store Rating: {avg_rating}"
)
