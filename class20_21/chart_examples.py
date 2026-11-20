import pandas as pd
import streamlit as st

st.title("Streamlit Chart Examples")

# Each row represents one year.
example_df = pd.DataFrame({
    "year": [2020, 2021, 2022, 2023],
    "average_rating": [7.0, 8.0, 8.0, 9.0],
    "rolling_rating": [7.0, 7.5, 7.67, 8.33],
    "movie_count": [2, 4, 3, 6],
})

st.dataframe(example_df, hide_index=True)

st.header("Bar chart: compare values")
st.bar_chart(example_df, x="year", y="movie_count")

st.header("Line chart: show a trend")
st.line_chart(example_df, x="year", y="average_rating")

st.header("Two lines: compare trends")
st.line_chart(
    example_df,
    x="year",
    y=["average_rating", "rolling_rating"],
)

st.header("Scatter plot: explore a relationship")
st.scatter_chart(example_df, x="movie_count", y="average_rating")