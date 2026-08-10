import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Developer Insights",
    page_icon="👨‍💻",
    layout="wide"
)

st.title("👨‍💻 Developer Insights")

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

try:
    df = pd.read_csv("data/googleplaystore.csv")
except FileNotFoundError:
    st.error("Dataset not found: data/googleplaystore.csv")
    st.stop()

# Clean column names
df.columns = df.columns.str.strip()

# --------------------------------------------------
# CHECK FOR DEVELOPER COLUMN
# --------------------------------------------------

developer_columns = [
    "Developer",
    "Developer Name",
    "Developer Id",
    "Developer ID",
    "Developer Email",
    "Developer_Name",
    "Developer_Name"
]

developer_col = None

for col in df.columns:
    if col.strip().lower() in [x.lower() for x in developer_columns]:
        developer_col = col
        break

# --------------------------------------------------
# IF DEVELOPER DATA EXISTS
# --------------------------------------------------

if developer_col is not None:

    st.success(f"Developer data found: {developer_col}")

    # Remove missing developer names
    developer_df = df.dropna(subset=[developer_col]).copy()

    # Top developers
    developers = (
        developer_df.groupby(developer_col)
        .agg(
            App_Count=("App", "count"),
            Average_Rating=("Rating", "mean"),
            Total_Reviews=("Reviews", "sum")
        )
        .reset_index()
        .sort_values("App_Count", ascending=False)
        .head(20)
    )

    # Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Developers",
        developer_df[developer_col].nunique()
    )

    col2.metric(
        "Total Apps",
        len(developer_df)
    )

    col3.metric(
        "Top Developer Apps",
        developers["App_Count"].max()
    )

    # Chart
    fig = px.bar(
        developers,
        x=developer_col,
        y="App_Count",
        title="Top Developers by Number of Apps",
        labels={
            developer_col: "Developer",
            "App_Count": "Number of Apps"
        }
    )

    fig.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Developer rating chart
    fig2 = px.bar(
        developers.sort_values(
            "Average_Rating",
            ascending=False
        ),
        x=developer_col,
        y="Average_Rating",
        title="Top Developers by Average Rating",
        labels={
            developer_col: "Developer",
            "Average_Rating": "Average Rating"
        }
    )

    fig2.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # Table
    st.subheader("Developer Statistics")

    developers["Average_Rating"] = developers[
        "Average_Rating"
    ].round(2)

    st.dataframe(
        developers,
        use_container_width=True
    )

# --------------------------------------------------
# CURRENT DATASET DOES NOT HAVE DEVELOPER DATA
# --------------------------------------------------

else:

    st.warning(
        "The current Google Play Store dataset does not contain "
        "a developer/publisher column."
    )

    st.info(
        "Developer-specific analysis cannot be calculated from "
        "this dataset. The dashboard is showing app-level insights instead."
    )

    # --------------------------------------------------
    # APP LEVEL METRICS
    # --------------------------------------------------

    st.subheader("📱 App-Level Insights")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Apps",
        df["App"].nunique()
    )

    col2.metric(
        "Categories",
        df["Category"].nunique()
    )

    col3.metric(
        "Average Rating",
        round(df["Rating"].mean(), 2)
    )

    col4.metric(
        "Total Reviews",
        f"{df['Reviews'].sum():,}"
    )

    # --------------------------------------------------
    # TOP APPS BY REVIEWS
    # --------------------------------------------------

    st.subheader("🔥 Most Reviewed Apps")

    top_apps = (
        df[["App", "Reviews", "Rating", "Category"]]
        .dropna(subset=["Reviews"])
        .sort_values(
            "Reviews",
            ascending=False
        )
        .head(20)
    )

    fig = px.bar(
        top_apps,
        x="Reviews",
        y="App",
        orientation="h",
        title="Top 20 Apps by Number of Reviews",
        hover_data=[
            "Rating",
            "Category"
        ]
    )

    fig.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------
    # CATEGORY PERFORMANCE
    # --------------------------------------------------

    st.subheader("📊 Category Performance")

    category_stats = (
        df.groupby("Category")
        .agg(
            App_Count=("App", "count"),
            Average_Rating=("Rating", "mean"),
            Total_Reviews=("Reviews", "sum")
        )
        .reset_index()
        .sort_values(
            "App_Count",
            ascending=False
        )
    )

    category_stats["Average_Rating"] = (
        category_stats["Average_Rating"].round(2)
    )

    fig2 = px.bar(
        category_stats.head(20),
        x="Category",
        y="App_Count",
        title="Number of Apps by Category"
    )

    fig2.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # --------------------------------------------------
    # RATING VS REVIEWS
    # --------------------------------------------------

    st.subheader("⭐ Rating vs Reviews")

    rating_df = df.dropna(
        subset=["Rating", "Reviews"]
    )

    fig3 = px.scatter(
        rating_df,
        x="Reviews",
        y="Rating",
        size="Reviews",
        hover_name="App",
        color="Category",
        title="App Rating vs Number of Reviews"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # --------------------------------------------------
    # DATASET COLUMNS
    # --------------------------------------------------

    with st.expander("🔎 Dataset Information"):

        st.write(
            "The current dataset contains the following columns:"
        )

        st.write(
            df.columns.tolist()
        )

        st.caption(
            "A real Developer column is required for "
            "developer-level analysis."
        )
