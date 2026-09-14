'''
SQLModel class, is a sub class of Pydentic BaseModel class, as such, it has all implementations of pydantic
'''
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from enum import Enum
from datetime import date


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


# --- Author Schemas ---
class AuthorBase(SQLModel):
    name: str
    section: str


class AuthorCreate(AuthorBase):
    """Payload data expected when a client creates an Author independently."""
    pass


class AuthorRead(AuthorBase):
    """Data sent back to the client for an Author."""
    id: int
    language_id: int


class Author(AuthorBase, table=True):
    """The database table mapping for Authors."""
    id: int = Field(default=None, primary_key=True)
    language_id: int = Field(foreign_key="language.id", ondelete="CASCADE")
    
    # Database relationships
    language: "Language" = Relationship(back_populates="authors")


# --- Language Schemas ---
class LanguageBase(SQLModel):
    name: str
    type: TypeChoices
    date_released: date | None


class LanguageCreate(LanguageBase):
    """Payload data expected when a client creates a Language."""
    authors: list[AuthorCreate] | None = None

    @field_validator('type', mode='before')
    def title_case_type(cls, value):
        if isinstance(value, str):
            return value.title()
        return value
    
class LanguageUpdate(LanguageBase):
    """Payload data expected when a client creates a Language."""
    authors: list[AuthorCreate] | None = None

    @field_validator('type', mode='before')
    def title_case_type(cls, value):
        if isinstance(value, str):
            return value.title()
        return value


class LanguageRead(LanguageBase):
    """Data sent back to the client for a basic Language profile."""
    id: int


class LanguageReadWithAuthors(LanguageRead):
    """Data sent back to the client when nested authors are requested."""
    authors: list[AuthorRead] = []


class Language(LanguageBase, table=True):
    """The database table mapping for Languages."""
    id: int = Field(default=None, primary_key=True)
    
    # Database relationships
    authors: list[Author] = Relationship(back_populates="language", cascade_delete=True)