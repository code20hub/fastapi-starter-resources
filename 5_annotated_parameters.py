'''
In this video, we'll explore the Annotated type in Python, and how it can be used to add metadata to an existing type.

Custom logic can then process that metadata and perform actions based on the values used!

We'll see how Annotated is used in FastAPI with the Query, Path, Header and Cookie parameters to handler functions,
and will dive deeper into the internals of the typing module to see how we can extract and process the metadata passed to Annotated.

Annotated do not get intepreted unless if there library has machannism to deal with them, i.e) provided implementation to interprete and use the annotation.
'''
from fastapi import FastAPI, HTTPException, Query, Path
from schemas import LanguageBase, LanguageID, LanguageCreate, TypeURLChoices
from typing import Annotated

app = FastAPI()

# List of objects
LANGS = [
	{
		"id": 1, "name": "Python", "type": "Interpreted",
		"authors": [
			{"name" : "Johannes", "section": "Introduction"},
			{"name" : "Johannes", "section": "Chapter 1"}
		]
	},
    {"id": 2, "name": "PHP", "type": "Interpreted"},
    {"id": 3, "name": "HTML", "type": "Markup"},
    {"id": 4, "name": "C++", "type": "Compiled"},
    {"id": 5, "name": "JavaScript", "type": "Interpreted"},
    {"id": 6, "name": "Java", "type": "Hybrid"},
    {"id": 7, "name": "Rust", "type": "Compiled"},
    {"id": 8, "name": "Go", "type": "Compiled"},
    {"id": 9, "name": "Ruby", "type": "Interpreted"}
]


@app.get('/')
def index() -> dict:
	return {'message': 'Hello World'}


# we can add return status code on the decorator itself, by default is 200 (OK)
# use the default list of languages also for filtering
# Annotated used to perform validatio on incoming query parameters
@app.get('/languages', status_code=200)
async def languages(
    type: TypeURLChoices | None = None, 
    has_authors: bool = False,
    q: Annotated[str | None, Query(max_length=50)] = None
) -> list[LanguageID]:
    
	languages_list = [LanguageID(**lang) for lang in LANGS]

	if type:
		languages_list = [lang for lang in languages_list if lang.type.value.lower() == type.value]
	
	# if has_authors:
	# 	languages_list = [lang for lang in languages_list if lang.authors is not None and len(lang.authors) > 0]

	if q:
		languages_list = [lang for lang in languages_list if q.lower() in lang.name.lower()]

	return languages_list

# Annotated used to add meta data to endpoints, and in coming parameters
@app.get('/language/{lang_id}')
async def language(lang_id: Annotated[int, Path(title="The Language ID")]) -> LanguageID:
    # The second argument (None) prevents an error if the ID doesn't exist
    # returns nex element in the array based on condition, else none
	language = next((LanguageID(**lang) for lang in LANGS if lang['id'] == lang_id), None)
	if language is None:
		raise HTTPException(404, detail='Language not found')

	return language

# add simple validation through Enums: useeful, when we do not want to search the datasets for things that do not exists
# within the dataset; i.e) a whitelisted - reject without even searching the dataset
@app.get('/langauges/type/{type}')
async def langauges_by_type(type: TypeURLChoices) -> list[LanguageID]:
    return [
        lang for lang in LANGS if lang['type'].lower() == type.value
	]


@app.post('/languages', status_code=201)
async def create_lnaguage(language_data: LanguageCreate) -> LanguageID:
    id = LANGS[-1]['id'] + 1
    
    # model_dump() - gives us back the dictionary to add to LANGS list
    language = LanguageID(id=id, **language_data.model_dump()).model_dump()
    LANGS.append(language)
    
    return language


