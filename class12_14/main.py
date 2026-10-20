import logging

from fastapi import FastAPI, Query

app = FastAPI(title="Movie API")

@app.get("/health")
def health_check():
    return {"status": "ok"}


#a path parameter identifies a resource (movie) to retrieve
@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int): #type annotation: it declares the expected type, int
    return {"requested_id": movie_id}


from fastapi import Query
#a query parameter adjusts a request
@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    #The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}


from models import MovieInput
@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    return movie.model_dump() #Converts the model to a Python dictionary.


from models import MovieResponse
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