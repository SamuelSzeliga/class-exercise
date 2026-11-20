import logging

import pandas as pd
import requests
import streamlit as st

from api_client import fetch_records

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

st.title("Movie Explorer")
st.write("Explore genre summaries and yearly rating trends.")

st.header("Which genres have the highest average ratings?")
min_movies = st.slider("Minimum movies per genre", 1, 6, 3)

try:
    records = fetch_records("/analysis/genres", {"min_movies": min_movies})
except requests.RequestException as error:
    logger.warning(f"Cannot retrieve genre summary: {error}")
    st.error("Cannot load genre data. Check that the API is running.")
    st.stop()

if not records:
    st.info("No genres match this minimum movie count.")
else:
    genre_df = pd.DataFrame(records)
    st.dataframe(genre_df, hide_index=True)
    st.bar_chart(genre_df, x="genre", y="average_rating")
    logger.info(f"Displayed genre summary: groups={len(genre_df)}")


st.header("How have ratings changed over time?")
window = st.slider("Rolling window (yearly observations)", 1, 6, 3)

try:
    records = fetch_records("/analysis/years", {"window": window})
except requests.RequestException as error:
    logger.warning(f"Cannot retrieve year trend: {error}")
    st.error("Cannot load year data. Check that the API is running.")
    st.stop()

if not records:
    st.info("No years match this window count.")
else:
    year_df = pd.DataFrame(records)
    st.dataframe(year_df, hide_index=True)
    st.header("Two lines: compare trends")
    st.line_chart(year_df, x="release_year", y=["average_rating", "rolling_rating"])

    logger.info(f"Displayed year trend: groups={len(genre_df)}")



st.header("Which movies meet your minimum rating?")
min_rating = st.slider("Minimum movie rating", 0.0, 10.0, 8.0, 0.5)

# TODO: Use fetch_records() to request /movies/filter with min_rating.
# Catch requests.RequestException, show an error, and call st.stop().
# If the list is empty, show an informational message.
# Otherwise, display the returned records as a DataFrame table.
# Log the displayed row count and minimum rating at INFO.
try:
    records = fetch_records("/movies/filter", {"min_rating": min_rating})
except requests.RequestException as error:
    logger.warning(f"Cannot retrieve movies: {error}")
    st.error("Cannot load year data. Check that the API is running.")
    st.stop()

if not records:
    st.info("No movie ratings match this min_rating.")
else:
    movie_df = pd.DataFrame(records)
    st.dataframe(movie_df, hide_index=True)

    logger.info(f"Displayed movies: groups={len(movie_df)}")
