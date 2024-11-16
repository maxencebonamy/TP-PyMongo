from fastapi import FastAPI
from dotenv import dotenv_values
from neo4j import GraphDatabase
from pymongo import MongoClient
from routers.movie_router import router as movie_router

config = dotenv_values(".env")
app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGODB_URL"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database")

    app.neo4j_driver = GraphDatabase.driver(config["NEO4J_URL"], auth=(config["NEO4J_USER"], config["NEO4J_PASSWORD"]))
    app.neo4j_driver.session()
    print("Connected to the Neo4j database")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    app.neo4j_driver.close()


app.include_router(movie_router, tags=["movies"], prefix="/movies")
