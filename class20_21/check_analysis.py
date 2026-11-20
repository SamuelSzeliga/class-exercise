from pathlib import Path
import pandas as pd
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

def summarize_genres(df, min_movies=1):
    summary = df.groupby("genre", as_index=False).agg(
        movie_count=("title", "count"),
        average_rating=("rating", "mean"),
    )
    summary = summary[summary["movie_count"]>=min_movies]
    summary = summary.sort_values(
        ["average_rating", "genre"], ascending=[False, True]
    )
    summary["average_rating"] = summary["average_rating"].round(2)
    logger.debug(f"Genre summary: groups={len(summary)}")
    return summary


def summarize_years(df, window):
    summary = df.groupby("release_year", as_index=False).agg(
        average_rating=("rating", "mean")
    )
    summary = summary.sort_values("release_year")

    summary["rolling_rating"] = summary["average_rating"].rolling(
        window=window, min_periods=1).mean()

    summary[["average_rating", "rolling_rating"]] = summary[
        ["average_rating", "rolling_rating"]].round(2)
    logger.debug(f"Year summary: years={len(summary)}, window={window}")
    return summary


def filter_movies(df, min_rating):

    df_new = df[df["rating"] >= min_rating]
    return df_new[["title", "release_year", "rating", "genre"]]


def main():
    df = pd.read_csv(Path("data") / "class20_movies.csv")
    print(df.groupby("genre")["rating"].mean())
    print(summarize_genres(df))
    print(summarize_years(df))


if __name__ == "__main__":
    main()