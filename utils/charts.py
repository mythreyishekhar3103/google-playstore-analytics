import plotly.express as px
import plotly.graph_objects as go


def top_categories_chart(df):

    top_categories = (
        df["Category"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_categories.columns = [
        "Category",
        "Apps"
    ]

    fig = px.bar(
        top_categories,
        x="Category",
        y="Apps",
        text="Apps",
        title="Top 10 Categories by Number of Apps"
    )

    return fig


def rating_distribution_chart(df):

    fig = px.histogram(
        df,
        x="Rating",
        nbins=30,
        title="Rating Distribution"
    )

    return fig


def installs_by_category_chart(df):

    installs = (
        df.groupby("Category")
        ["Maximum Installs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.pie(
        installs,
        names="Category",
        values="Maximum Installs",
        title="Installs Share by Category"
    )

    return fig


def average_rating_chart(df):

    ratings = (
        df.groupby("Category")
        ["Rating"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        ratings,
        x="Category",
        y="Rating",
        title="Highest Rated Categories"
    )

    return fig


def developer_chart(df):

    developers = (
        df.groupby("Developer Id")
        .size()
        .sort_values(ascending=False)
        .head(15)
        .reset_index(name="Apps")
    )

    fig = px.bar(
        developers,
        x="Developer Id",
        y="Apps",
        title="Top Developers by App Count"
    )

    return fig


def correlation_heatmap(df):

    columns = [
        "Rating",
        "Rating Count",
        "Maximum Installs",
        "Minimum Installs"
    ]

    available_cols = [
        col for col in columns
        if col in df.columns
    ]

    corr = df[available_cols].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Heatmap"
    )

    return fig


def category_treemap(df):

    apps = (
        df.groupby("Category")
        .size()
        .reset_index(name="Apps")
    )

    fig = px.treemap(
        apps,
        path=["Category"],
        values="Apps",
        title="Category Market Share"
    )

    return fig
