from enum import Enum
from pydantic import BaseModel


# enum types give us built in validation for filtering
class TypeURLChoices(Enum):
    INTERPRETED = 'interpreted'
    MARKUP = 'markup'
    COMPILED = 'compiled'
    HYBRID = 'hybrid'

class Author(BaseModel):
    name: str
    section: str

class Languange(BaseModel):
    id: int
    name: str
    type: str
    authors: list[Author] = None