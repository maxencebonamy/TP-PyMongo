from fastapi import APIRouter
from fastapi import Request, Response
from models.movie import Movie
from models.pagination import PaginationResponse
import utils.utils as utils
from bson.regex import Regex

router = APIRouter()


@router.get("/", response_description="Index movies", response_model=PaginationResponse[Movie])
def index_artists(request: Request):
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
