from enum import Enum
from pydantic import BaseModel, field_validator


# enum types give us built in validation for filtering
class TypeURLChoices(Enum):
    INTERPRETED = 'interpreted'
    MARKUP = 'markup'
    COMPILED = 'compiled'
    HYBRID = 'hybrid'
    
class TypeChoices(Enum):
    INTERPRETED = 'Interpreted'
    MARKUP = 'Markup'
    COMPILED = 'Compiled'
    HYBRID = 'Hybrid'

class Author(BaseModel):
    name: str
    section: str

class LanguageBase(BaseModel):
    name: str
    type: TypeChoices #
    authors: list[Author] = []
    
class LanguageID(LanguageBase):
    id: int

# validation used in Pydantic model for pre validation.
# this ensures that tytle is always Title Case before processed, useful is user
# send type as 'hybrid' or 'HYBRID' = Hybrid
class LanguageCreate(LanguageBase):
    @field_validator('type', mode='before')
    def title_case_type(cls, value):
        return value.title()