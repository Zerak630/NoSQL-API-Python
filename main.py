from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from neo4j import GraphDatabase, basic_auth

from router_movie import router as movies_router

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    
    print("Connecting to MongoDB database...")
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["ATLAS_DB_NAME"]]

    app.include_router(movies_router, tags=["movies"], prefix="/movie")

    print("Connected to the Atlas personal MongoDB database!")

    print("Connecting to Neo4j database...")

    app.neo_client = GraphDatabase.driver(
        config["NEO4J_URI"],
        auth=basic_auth(config["NEO4J_USER"], config["NEO4J_PASSWORD"]))

    print("Connected to Neo4j database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    app.neo_client.close()