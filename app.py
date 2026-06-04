import streamlit as st
from utils.data_loader import load_data, get_basic_stats
from utils.charts import (
    top_categories_chart,
    rating_distribution_chart,
    installs_by_category_chart
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Google Play Store Analytics",
    page_icon="📱",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

[data-testid="metric-container"]{
    background-color:white;
    border:1px solid #e6e6e6;
    padding:15px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.05);
}

h1,h2,h3{
    color:#1f4e79;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
df = load_data()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.title("📊 Dashboard Filters")

categories = st.sidebar.multiselect(
    "Select Categories",
    sorted(df["Category"].dropna().unique())
)

free_paid = st.sidebar.selectbox(
    "App Type",
    ["All", "Free", "Paid"]
)

# Apply Filters
filtered_df = df.copy()

if categories:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(categories)
    ]

if free_paid == "Free":
    filtered_df = filtered_df[
        filtered_df["Free"] == True
    ]

elif free_paid == "Paid":
    filtered_df = filtered_df[
        filtered_df["Free"] == False
    ]

# --------------------------------------------------
# Dashboard Header
# --------------------------------------------------
st.title("📱 Google Play Store Analytics Dashboard")
st.markdown(
    "Analyze Play Store applications, ratings, installs, categories and developer insights."
)

# --------------------------------------------------
# KPI Metrics
# --------------------------------------------------
stats = get_basic_stats(filtered_df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📱 Total Apps",
        f"{stats['total_apps']:,}"
    )

with col2:
    st.metric(
        "📂 Categories",
        stats["total_categories"]
    )

with col3:
    st.metric(
        "⭐ Avg Rating",
        stats["average_rating"]
    )

with col4:
    st.metric(
        "⬇️ Total Installs",
        f"{stats['total_installs']:,}"
    )

st.divider()

# --------------------------------------------------
# Charts Row 1
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        top_categories_chart(filtered_df),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        rating_distribution_chart(filtered_df),
        use_container_width=True
    )

# --------------------------------------------------
# Charts Row 2
# --------------------------------------------------
st.plotly_chart(
    installs_by_category_chart(filtered_df),
    use_container_width=True
)

# --------------------------------------------------
# Insights Section
# --------------------------------------------------
st.subheader("📌 Quick Insights")

try:
    most_apps_category = (
        filtered_df["Category"]
        .value_counts()
        .idxmax()
    )

    highest_rating_category = (
        filtered_df.groupby("Category")["Rating"]
        .mean()
        .idxmax()
    )

    st.success(f"""
    ✅ Category with Most Apps: **{most_apps_category}**

    ✅ Highest Rated Category: **{highest_rating_category}**

    ✅ Average Rating: **{stats['average_rating']}**

    ✅ Total Categories: **{stats['total_categories']}**
    """)

except:
    st.warning("No data available for selected filters.")

# --------------------------------------------------
# Dataset Preview
# --------------------------------------------------
st.subheader("📄 Dataset Preview")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption(
    "Google Play Store Analytics Dashboard | Built with Streamlit, Pandas & Plotly"
)
