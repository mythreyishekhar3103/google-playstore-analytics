import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    """
    Load and clean Google Play Store dataset
    """

    df = pd.read_csv("data/Google-Playstore.csv")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Convert numeric columns
    numeric_cols = [
        "Rating",
        "Rating Count",
        "Maximum Installs",
        "Minimum Installs",
        "Price"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # Handle missing values
    if "Rating" in df.columns:
        df["Rating"] = df["Rating"].fillna(
            df["Rating"].median()
        )

    return df


def get_basic_stats(df):
    """
    Returns key dashboard metrics
    """

    stats = {
        "total_apps": len(df),
        "total_categories": df["Category"].nunique(),
        "average_rating": round(df["Rating"].mean(), 2),
        "total_installs": int(df["Maximum Installs"].sum())
    }

    return stats
