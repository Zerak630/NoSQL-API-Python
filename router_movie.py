from typing import List
from fastapi import APIRouter, Body, Request, Response, HTTPException, status

from model_movie import Movie, MovieUpdate

router = APIRouter()

@router.get("/", description="List all movies", response_model=List[Movie])
def list_all_movies(request: Request):
    """
        Return a list with all movies stored in MongoDB database
    """    
    movies = list(request.app.database["movies"].find(limit=100)) # works until 692nd movie, validation error on it
    return movies

@router.get("/compare", description="Compare how many movies are in both databases", response_model=int)
def compare_movies(request: Request):
    # get all movies titles from mongodb and make a list of them
    mongo_titles = list(request.app.database["movies"].find(projection={"_id":0, "title": 1}))

    # same with neo4j
    cypher_query = '''
        MATCH (m:Movie)
        RETURN distinct m.title as title
    '''

    with request.app.neo_client.session(database="neo4j") as session:
        neo_titles = session.read_transaction(
            lambda tx: tx.run(cypher_query).data())

    # compare both lists
    cpt = 0
    for m in mongo_titles:
        if m in neo_titles:
            cpt += 1
    return cpt

@router.get("/{name}", description="List a specific movie by movie name or actor name", response_model=Movie)
def list_movie_by_title_or_actor(name: str, request: Request):
    return request.app.database["movies"].find_one({ "$or": [{"title": name}, {"cast": name}]})

@router.get("/raters/{movie}", description="List all reviewers for a movie")
def list_reviewers_by_movie(movie: str, request: Request):
    cypher_query = '''
        MATCH (reviewer:Person)-[:REVIEWED]->(movie:Movie {title:$favorite})
        RETURN distinct reviewer.name as name LIMIT 20
    '''
    with request.app.neo_client.session(database="neo4j") as session:
        results = session.read_transaction(
            lambda tx: tx.run(cypher_query,
                            favorite=movie).data())
    return results

@router.get("/rater/{rater_name}", description="List movies reviewed by given person")
def list_movies_reviewed_by_reviewer(rater_name: str, request: Request):
    cypher_query= '''
        MATCH (p:Person {name:$name})-[:REVIEWED]->(m:Movie)
        RETURN p.name AS `Person`, size(collect(m.title)) AS `Number of Reviews`, collect(m.title) AS `Movies`
    '''

    with request.app.neo_client.session(database="neo4j") as session:
        results = session.read_transaction(
            lambda tx: tx.run(cypher_query,
                            name=rater_name).data())
    return results




@router.post("/{name}", description="Update a movie with a given title", response_model=Movie)
def update_movie(name: str, request: Request, movie_update: MovieUpdate = Body(...)):

    updated_fields = {k: v for k, v in movie_update.dict(exclude_none=True).items()} # remove unset fields

    update_result = request.app.database["movies"].update_one({"title": name}, {"$set": updated_fields}) # update the movie

    if update_result.modified_count == 0: # check if the movie has been updated
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie '{name}' not found") # raise HTTP exception if not found

    if (
        existing_movie := request.app.database["movies"].find_one({"title": name}) # find the updated movie
    ) is not None:
        return existing_movie
    return None