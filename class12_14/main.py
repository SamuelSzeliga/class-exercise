import logging
from fastapi import FastAPI, Query
from fastapi import File, UploadFile
from fastapi import HTTPException
from fastapi import Query
from pathlib import Path
import io
import pandas as pd
from src._init_ import DataStorage, CSVInfo
from src._init_ import ProcessConfig
import pandas as pd
from middleware import log_requests


app = FastAPI(title="Movie API")
app.middleware("http")(log_requests)

@app.get("/health")
def health_check():
    return {"status": "ok"}


#a path parameter identifies a resource (movie) to retrieve
@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int): #type annotation: it declares the expected type, int
    return {"requested_id": movie_id}


#a query parameter adjusts a request
@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    #The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}


from src.models import MovieInput
@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    return movie.model_dump() #Converts the model to a Python dictionary.


from src.models import MovieResponse
demo_movie_examples = []
@app.post("/demo/movie-examples", response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    demo_movie_examples.append(record)
    return record


import logging
logging.basicConfig(
level=logging.INFO,
format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

movies = {
    1: {"id": 1, "title": "Movie A", "release_year": 2020},
    2: {"id": 2, "title": "Movie B", "release_year": 2021},
}


@app.get("/movies", response_model=list[MovieResponse])
def list_movies(limit: int = Query(default=2, ge=1)):

    list_of_dictionaries = list(movies.values())
    out = list_of_dictionaries[:limit]
    logger.info(f"{len(out)} movies")
    return out


@app.post("/movies", response_model=MovieResponse)
def add_movie(movie: MovieInput):
    
    movie_id = len(movies) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    movies[movie_id] = record
    return record


@app.post("/demo/inspect-csv")
async def demo_inspect_csv(file: UploadFile = File(...)):
    # ... in File(...) means the upload is required.
    contents = await file.read() # reads as bytes e.g. b"title,year\nMovie A,2020\n"
    return {"filename": file.filename,"size_bytes": len(contents)}


@app.get("/demo/movie-lookup/{movie_id}", response_model=MovieResponse)
def demo_lookup_movie(movie_id: int):
    movie = movies.get(movie_id)

    if movie is None:
        logger.warning(f"Movie not found: {movie_id}")
        raise HTTPException( status_code=404, detail="Movie not found")

    return movie


storage = DataStorage()

@app.post("/inspect-csv", response_model=CSVInfo)
async def inspect_csv(file: UploadFile = File(...)):

    #check the filename extension
    if Path(file.filename).suffix.lower() != ".csv":
        logger.warning("Non-CSV file uploaded")
        raise HTTPException( status_code=400, detail="Non-CSV file uploaded")

    #read the data
    contents = await file.read()

    #try parsing
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except (pd.errors.EmptyDataError,pd.errors.ParserError,UnicodeDecodeError) as error:
        logger.warning(f"Cannot read CSV: {error}")
        raise HTTPException(status_code=400, detail="Cannot read the uploaded CSV")

    #save data
    movie_id = storage.save_data(df, file.filename)
    logger.info(f"MovieData {file.filename} (ID {movie_id}) saved")

    #return a CSVinfo object with the ID, filename, shape, and column names
    return CSVInfo(filename=file.filename,
                   rows=df.shape[0], columns=df.shape[1],
                   column_names=list(df.columns),
                   dataset_id=movie_id)


@app.get("/datasets/{dataset_id}/shape")
def get_dataset_shape(dataset_id: int):
    result = storage.get_data()
    if result is None:
        logger.warning(f"ID not found: {dataset_id}")
        raise HTTPException( status_code=404, detail="Not found")
    logger.info("Id found!")

    return {"dataset_id":dataset_id,
            "rows":result.shape[0],
            "cols":result.shape[1]}

@app.post("/demo/process-config")
def demo_process_config(config: ProcessConfig):
    df = pd.DataFrame({"title": ["Movie A", "Movie A", "Movie B", None]})
    settings = config.model_dump()

    if settings["processing"]["remove_duplicates"]:
        df = df.drop_duplicates()
    if settings["processing"]["drop_missing"]:
        df = df.dropna()

    return {"rows": len(df)}