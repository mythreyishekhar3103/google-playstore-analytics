import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Smart Insights")

# Load dataset
try:
    df = pd.read_csv("data/googleplaystore.csv")
except FileNotFoundError:
    st.error("Dataset not found in data/googleplaystore.csv")
    st.stop()

# Clean column names
df.columns = df.columns.str.strip()

# Show columns for debugging
with st.expander("Available Columns"):
    st.write(df.columns.tolist())

# Find installs column
installs_col = None

for col in [
    "Maximum Installs",
    "Installs",
    "Maximum_Installs"
]:
    if col in df.columns:
        installs_col = col
        break

# Convert installs column if found
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

# Find app name column
app_col = None

for col in [
    "App Name",
    "App",
    "App_Name"
]:
    if col in df.columns:
        app_col = col
        break

# Most Installed App
if installs_col and app_col and "Category" in df.columns:

    highest = df.loc[
        df[installs_col].idxmax()
    ]

    st.success(
        f"""
Most Installed App: {highest[app_col]}

Category: {highest['Category']}

Installs: {int(highest[installs_col]):,}
"""
    )

else:
    st.warning(
        "Could not identify installs column or app name column."
    )

# Most Popular Category
if "Category" in df.columns:

    top_category = (
        df["Category"]
        .value_counts()
        .idxmax()
    )

    st.info(
        f"Most Popular Category: {top_category}"
    )

# Average Rating
if "Rating" in df.columns:

    df["Rating"] = pd.to_numeric(
        df["Rating"],
        errors="coerce"
    )

    avg_rating = round(
        df["Rating"].mean(),
        2
    )

    st.warning(
        f"Average Play Store Rating: {avg_rating}"
    )

# Extra Insights
st.subheader("📊 Dataset Summary")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Apps",
    len(df)
)

if "Category" in df.columns:
    col2.metric(
        "Categories",
        df["Category"].nunique()
    )

if "Rating" in df.columns:
    col3.metric(
        "Average Rating",
        round(df["Rating"].mean(), 2)
    )
