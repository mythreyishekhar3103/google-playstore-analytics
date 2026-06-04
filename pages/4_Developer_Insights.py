# Use Category instead of Developer
developer_col = "Category"

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
    "Total Categories",
    developers[developer_col].nunique()
)

col2.metric(
    "Top Categories",
    len(developers)
)

# Chart
fig = px.bar(
    developers,
    x=developer_col,
    y="App Count",
    title="Top Categories by App Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Data Table
st.subheader("Category Statistics")

st.dataframe(
    developers,
    use_container_width=True
)
