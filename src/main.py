from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routers.movie_router import router as movie_router

config = dotenv_values(".env")
app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGODB_URL"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(movie_router, tags=["movies"], prefix="/movies")
