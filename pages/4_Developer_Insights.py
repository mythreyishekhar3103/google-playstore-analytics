import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Developer Insights",
    page_icon="👨‍💻",
    layout="wide"
)

st.title("👨‍💻 Developer Insights")

# Load dataset
df = pd.read_csv("data/googleplaystore.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Possible developer columns
developer_col = None

possible_columns = [
    "Developer Id",
    "Developer Name",
    "Developer",
    "Developer Email"
]

for col in possible_columns:
    if col in df.columns:
        developer_col = col
        break

# If no developer column exists
if developer_col is None:
    st.error("No developer-related column found in dataset.")

    st.subheader("Available Columns")
    st.write(df.columns.tolist())

    st.stop()

# Top developers
developers = (
    df.groupby(developer_col)
      .size()
      .reset_index(name="App Count")
      .sort_values(
          by="App Count",
          ascending=False
      )
      .head(20)
)

# Metrics
col1, col2 = st.columns(2)

col1.metric(
    "Total Developers",
    developers[developer_col].nunique()
)

col2.metric(
    "Top 20 Developers",
    len(developers)
)

# Chart
fig = px.bar(
    developers,
    x=developer_col,
    y="App Count",
    title="Top Developers by App Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Data Table
st.subheader("Developer Statistics")

st.dataframe(
    developers,
    use_container_width=True
)
