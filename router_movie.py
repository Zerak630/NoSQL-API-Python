from typing import List

from fastapi import APIRouter, Request

from model_movie import Movie

router = APIRouter()

@router.get("/all", response_description="List all movies", response_model=List[Movie])
def list_artists(request: Request):
    movies = list(request.app.database["movies"].find(limit=100))
    return movies

@router.get("/raters/{movie}", response_description="List all reviewers for a movie")
def list_reviewers(movie: str, request: Request):
    cypher_query = '''
        MATCH (reviewer:Person)-[:REVIEWED]->(movie:Movie {title:$favorite})
        RETURN distinct reviewer.name as name LIMIT 20
    '''
    with request.app.neo_client.session(database="neo4j") as session:
        results = session.read_transaction(
            lambda tx: tx.run(cypher_query,
                            favorite=movie).data())
    return results

@router.get("/rater/{rater_name}", response_description="List movies reviewed by given person")
def list_movies_reviewed(rater_name: str, request: Request):
    cypher_query= '''
        MATCH (p:Person {name:$name})-[:REVIEWED]->(m:Movie)
        RETURN p.name AS `Person`, size(collect(m.title)) AS `Number of Reviews`, collect(m.title) AS `Movies`
    '''

    with request.app.neo_client.session(database="neo4j") as session:
        results = session.read_transaction(
            lambda tx: tx.run(cypher_query,
                            name=rater_name).data())
    return results