import uuid
from pydantic import BaseModel, Field

class Artist(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    first_name: str = None
    last_name: str = None
    birth_date: str | None = None
    hobbies: list[str] | None = None

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "artist:9999",
                "first_name": "Don Quixote",
                "last_name": "Miguel de Cervantes",
                "birth_date": "2000",
                "hobbies": ["golf", "poney", "hockey"]
            }
        }

class ArtistUpdate(BaseModel):
    first_name: str | None
    last_name: str | None
    birth_date: str | None
    hobbies: list[str] | None


    class Config:
        schema_extra = {
            "example": {
                "first_name": "Don Quixote",
                "last_name": "Miguel de Cervantes",
                "birth_date": "2000",
                "hobbies": ["golf", "poney", "hockey"]
            }
        }