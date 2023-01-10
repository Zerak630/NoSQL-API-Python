from datetime import datetime
import uuid
from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional, Union
from pydantic import BaseModel, Field


class Award(BaseModel):
    nominations: Optional[int]
    text: Optional[str]
    wins: Optional[int]

    class Config:
        orm_mode = True


class Imdb(BaseModel):
    id: Optional[int]
    rating: Optional[float]
    votes: Optional[int]

    class Config:
        orm_mode = True


class Critic(BaseModel):
    meter: Optional[int]
    numReviews: Optional[int]
    rating: Optional[float]

    class Config:
        orm_mode = True


class Viewer(BaseModel):
    meter: Optional[int]
    numReviews: Optional[int]
    rating: Optional[float]

    class Config:
        orm_mode = True


class Tomatoes(BaseModel):
    boxOffice: Optional[str]
    consensus: Optional[str]
    critic: Optional[Union[Critic, None]]
    dvd: Optional[datetime]
    fresh: Optional[int]
    lastUpdated: Optional[datetime]
    production: Optional[str]
    rotten: Optional[int]
    viewer: Optional[Union[Viewer, None]]
    website: Optional[str]

    class Config:
        orm_mode = True


class ObjId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        try:
            return cls(v)
        except InvalidId:
            raise ValueError("Not a valid ObjectId")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Movie(BaseModel):
    id: Union[ObjId, None] = Field(alias="_id")
    awards: Optional[Union[Award, None]]
    cast: Optional[list[str]]
    countries: Optional[list[str]]
    directors: Optional[list[str]]
    fullplot: Optional[str]
    plot: Optional[str]
    genres: Optional[list[str]]
    imdb: Optional[Union[Imdb, None]]
    languages: Optional[list[str]]
    lastupdated: Optional[str]
    metacritic: Optional[int]
    num_mflix_comments: Optional[int]
    poster: Optional[str]
    rated: Optional[str]
    released: Optional[datetime]
    runtime: Optional[int]
    title: Optional[str]
    tomatoes: Optional[Union[Tomatoes, None]]
    type: Optional[str]
    writers: Optional[list[str]]
    year: Optional[int]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjId: str
        }
        schema_extra = {
            "id":  "573a1390f29313caabcd42e8",
            "plot": "A group of bandits stage a brazen train hold-up, only to find a determined posse hot on their heels.",
            "genres": [
                "Short",
                "Western"
            ],
            "runtime": 11,
            "cast": [
                "A.C. Abadie",
                "Gilbert M. 'Broncho Billy' Anderson",
                "George Barnes",
                "Justus D. Barnes"
            ],
            "poster": "https://m.media-amazon.com/images/M/MV5BMTU3NjE5NzYtYTYyNS00MDVmLWIwYjgtMmYwYWIxZDYyNzU2XkEyXkFqcGdeQXVyNzQzNzQxNzI@._V1_SY1000_SX677_AL_.jpg",
            "title": "The Great Train Robbery",
            "fullplot": "Among the earliest existing films in American cinema - notable as the first film that presented a narrative story to tell - it depicts a group of cowboy outlaws who hold up a train and rob the passengers. They are then pursued by a Sheriff's posse. Several scenes have color included - all hand tinted.",
            "languages": [
                "English"
            ],
            "released": {
                "$date": {
                    "$numberLong": "-2085523200000"
                }
            },
            "directors": [
                "Edwin S. Porter"
            ],
            "rated": "TV-G",
            "awards": {
                "wins": 1,
                "nominations": 0,
                "text": "1 win."
            },
            "lastupdated": "2015-08-13 00:27:59.177000000",
            "year": 1903,
            "imdb": {
                "rating": 7.4,
                "votes": 9847,
                "id": 439
            },
            "countries": [
                "USA"
            ],
            "type": "movie",
            "tomatoes": {
                    "viewer": {
                        "rating": 3.7,
                        "numReviews": 2559,
                        "meter": 75
                    },
                "fresh": 6,
                "critic": {
                        "rating": 7.6,
                        "numReviews": 6,
                        "meter": 100
                    },
                "rotten": 0,
                "lastUpdated": {
                        "$date": {
                            "$numberLong": "1439061370000"
                        }
                    }
            },
            "num_mflix_comments": 0
        }