from typing import List

from fastapi import APIRouter, Request

from model_movie import Movie

router = APIRouter()

@router.get("/all", response_description="List all movies", response_model=List[Movie])
def list_artists(request: Request):
    movies = list(request.app.database["movies"].find(limit=100))
    return movies