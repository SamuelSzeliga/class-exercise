import logging
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Query

from check_analysis import summarize_genres, summarize_years

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Movie Analysis API")
df = pd.read_csv(Path("data") / "class20_movies.csv")


@app.get("/analysis/genres", response_model=list[dict])
def get_genres(min_movies: int = Query(default=1, ge=1)):

    result = summarize_genres(df, min_movies)
    logger.info(f"Returned genre summary: groups={len(result)}")
    return result.to_dict(orient="records")


@app.get("/analysis/years", response_model=list[dict])
def get_years(window: int = Query(default=3, ge=1)):

    result = summarize_years(df, window)
    logger.info(f"Returned summary: year count={len(result)}, window={window}")
    return result.to_dict(orient="records")