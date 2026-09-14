'''
SQLModel is a wrapper library—built on top of both SQLAlchemy and Pydantic—designed to eliminate duplicate code by letting a single class 
function as both a database table and a data validation schema.

It is based on Python-typed annotations.

Lisespan Events: used to execute loginc before and after the application starts, execute once at the begining and ending of thee application

'''
from fastapi import FastAPI, HTTPException, Query, Path, Depends
from models import (LanguageCreate, LanguageUpdate, Language, Author, TypeURLChoices, LanguageReadWithAuthors)
from typing import Annotated
from contextlib import asynccontextmanager
from db import init_db, get_session
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload


# runs once before app start, and after app comcludes/finish
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get('/')
def index() -> dict:
	return {'message': 'Hello World'}

# Annotated used to perform validatio on incoming query parameters
@app.get('/languages', status_code=200, response_model=list[LanguageReadWithAuthors])
async def languages(
    type: TypeURLChoices | None = None, 
    q: Annotated[str | None, Query(max_length=50)] = None,
    session: Session = Depends(get_session)
) -> list[Language]:
    
	# Use database-level sorting and filtering with joinedload to solve performance issues
	statement = select(Language).options(joinedload(Language.authors))

	if type:
		# Match against database enum storage values
		statement = statement.where(Language.type == type.value.title())
	if q:
		# Perform a case-insensitive search right in the database query
		statement = statement.where(Language.name.ilike(f"%{q}%"))
		
	languages_list = session.exec(statement).unique().all()

	return languages_list

# Annotated used to add meta data to endpoints, and in coming parameters
@app.get('/language/{lang_id}', response_model=LanguageReadWithAuthors)
async def language(
    lang_id: Annotated[int, Path(title="The Language ID")],
    session: Session = Depends(get_session)
) -> Language:
    
	# Eagerly load authors to avoid extra hidden database queries
    statement = select(Language).where(Language.id == lang_id).options(joinedload(Language.authors))
    language_obj = session.exec(statement).unique().first()
    
    if language_obj is None:
        raise HTTPException(404, detail='Language not found')

    return language_obj

@app.post('/languages', status_code=201, response_model=LanguageReadWithAuthors)
async def create_language(
    payload: LanguageCreate,
    session: Session = Depends(get_session)
) -> Language:
    
	# Create the base language
	language = Language(
		name=payload.name, 
		type=payload.type
	)
	session.add(language)
	session.flush()

    # Loop through and append authors, assigning the new language ID
	if payload.authors:
		for author_info in payload.authors:
			author = Author(
				name=author_info.name,
				section=author_info.section,
				language_id=language.id # Link it here automatically
			)
			session.add(author)
    
	# commit the session to save data into database
	session.commit()
	# refresh language to get db data; i.e) this gets the id from db
	session.refresh(language)

	return language


@app.put('/language/{lang_id}', response_model=LanguageReadWithAuthors)
async def update_language_full(
    lang_id: Annotated[int, Path(title="The Language ID")],
    payload: LanguageUpdate,
    session: Session = Depends(get_session)
) -> Language:
    statement = select(Language).where(Language.id == lang_id).options(joinedload(Language.authors))
    language = session.exec(statement).unique().first()

    if not language:
        raise HTTPException(status_code=404, detail="Language not found")

    # Replace scalar attributes
    language.name = payload.name
    language.type = payload.type

    # Replace relationships: Clear old authors and append new ones
    language.authors.clear()
    if payload.authors:
        for author_info in payload.authors:
            author = Author(
                name=author_info.name,
                section=author_info.section,
                language_id=language.id
            )
            session.add(author)

    session.commit()
    session.refresh(language)
    return language


@app.patch('/language/{lang_id}', response_model=LanguageReadWithAuthors)
async def update_language_partial(
    lang_id: Annotated[int, Path(title="The Language ID")],
    payload: LanguageUpdate,
    session: Session = Depends(get_session)
) -> Language:
    statement = select(Language).where(Language.id == lang_id).options(joinedload(Language.authors))
    language = session.exec(statement).unique().first()

    if not language:
        raise HTTPException(status_code=404, detail="Language not found")

    # Exclude unset fields to only update provided attributes
    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "authors" and value is not None:
            # Overwrite relationships if explicitly provided
            language.authors.clear()
            for author_info in payload.authors:
                author = Author(
                    name=author_info.name,
                    section=author_info.section,
                    language_id=language.id
                )
                session.add(author)
        elif key != "authors":
            setattr(language, key, value)

    session.commit()
    session.refresh(language)
    return language


@app.delete('/language/{lang_id}', status_code=204)
async def delete_language(
    lang_id: Annotated[int, Path(title="The Language ID")],
    session: Session = Depends(get_session)
) -> None:
    language = session.get(Language, lang_id)

    if not language:
        raise HTTPException(status_code=404, detail="Language not found")

    session.delete(language)
    session.commit()
    return None

