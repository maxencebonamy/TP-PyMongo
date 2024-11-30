from fastapi import APIRouter, Request, HTTPException, status, Response
from models.movie import Movie
from models.pagination import PaginationResponse
import utils.utils as utils
from bson.regex import Regex

router = APIRouter()


@router.get("/", response_description="Index movies", response_model=PaginationResponse[Movie])
def index_movies(request: Request):
    # Get the query parameters (pagination and filters)
    page = request.query_params.get("page")
    limit = request.query_params.get("limit")
    title_filter = request.query_params.get("title_filter")
    actor_filter = request.query_params.get("actor_filter")

    # Create the query based on the filters
    query = {}
    if title_filter:
        query["title"] = {"$regex": Regex(title_filter, "i")}
    if actor_filter:
        query["cast"] = {"$elemMatch": {"$regex": Regex(actor_filter, "i")}}

    # Paginate the movies
    collection = request.app.database["movies"]
    return utils.paginate(collection, query, page, limit)


@router.patch("/{title}", response_description="Update a movie", response_model=None)
async def update_movie(title: str, request: Request):
    collection = request.app.database["movies"]

    # Find the movie by title, if it does not exist return 404
    movie = collection.find_one({"title": title})
    if movie is None:
        return Response(status_code=404)

    # Update the movie with the new data
    update_data = await request.json()
    collection.update_one({"title": title}, {"$set": update_data})

    return {"message": "Updated successfully"}

@router.get("/common", response_description="Return the number of movies common between MongoDB and Neo4j")
def common_movies(request: Request):
    # Get all unique movie titles from MongoDB
    mongo_movies = set(request.app.database["movies"].distinct("title"))

    # Query Neo4j for all movie titles
    with request.app.neo4j_driver.session() as session:
        result = session.run("MATCH (m:Movie) RETURN m.title AS title")
        neo4j_titles = {record["title"] for record in result}

    # Calculate the intersection of MongoDB and Neo4j movie titles
    common_count = len(mongo_movies & neo4j_titles)
    return {"common_movies_count": common_count}


@router.get("/people_who_rated", response_description="List people who rated a given movie")
def people_who_rated(title: str, request: Request):
    # Query Neo4j for users who rated the given movie
    query = """
    MATCH (p:Person)-[rel]->(m:Movie{title: $title})
    WHERE rel.rating IS NOT NULL
    RETURN p.name AS name
    """
    with request.app.neo4j_driver.session() as session:
        result = session.run(query, title=title)
        people = [record["name"] for record in result]

    # Raise exception if no users found
    if not people:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No person found who rated the movie '{title}'")
    return {"people": people}


@router.get("/rating", response_description="Get a person with the number of movies they rated and the list of movies")
def person_ratings(person_name: str, request: Request):
    # Query Neo4j for movies rated by the specified person
    query = """
    MATCH (p:Person {name: $person_name})-[r:REVIEWED]->(m:Movie)
    RETURN m.title AS movie_title
    """
    with request.app.neo4j_driver.session() as session:
        result = session.run(query, person_name=person_name)
        ratings = [record["movie_title"] for record in result]

    # Raise exception if no ratings found for the person
    if not ratings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No ratings found for '{person_name}'")

    return {"person": person_name, "rated_count": len(ratings), "rated_movies": ratings}
