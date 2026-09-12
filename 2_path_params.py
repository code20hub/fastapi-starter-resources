from fastapi import FastAPI, HTTPException
from enum import Enum

app = FastAPI()

# List of objects
LANGS = [
	{"id": 1, "name": "Python", "type": "Interpreted"},
    {"id": 2, "name": "PHP", "type": "Interpreted"},
    {"id": 3, "name": "HTML", "type": "Markup"},
    {"id": 4, "name": "C++", "type": "Compiled"},
    {"id": 5, "name": "JavaScript", "type": "Interpreted"},
    {"id": 6, "name": "Java", "type": "Hybrid"},
    {"id": 7, "name": "Rust", "type": "Compiled"},
    {"id": 8, "name": "Go", "type": "Compiled"},
    {"id": 9, "name": "Ruby", "type": "Interpreted"}
]

class TypeURLChoices(Enum):
    INTERPRETED = 'interpreted'
    MARKUP = 'markup'
    COMPILED = 'compiled'
    HYBRID = 'hybrid'



@app.get('/')
def index() -> dict:
	return {'message': 'Hello World'}


# we can add return status code on the decorator itself, by default is 200 (OK)
@app.get('/languages', status_code=200)
async def languages() -> list[dict]:
	return LANGS

# Type-hints: to constrain values pass to parameters: throes an error is anything other integer is passed
@app.get('/language/{lang_id}')
async def language(lang_id: int) -> dict:
    # The second argument (None) prevents an error if the ID doesn't exist
	language = next((lang for lang in LANGS if lang['id'] == lang_id), None)
	if language is None:
        # HTTP Exception class, used mainly to send errors to the client    
		raise HTTPException(404, detail='Language not found')

	return language

''' 
	Add simple validation through Enums: useeful, when we do not want to search the datasets for things that do not exists
	within the dataset; i.e) a whitelisted - reject without even searching the dataset
'''
@app.get('/langauges/type/{type}')
async def langauges_by_type(type: TypeURLChoices) -> list[dict]:
    return [lang for lang in LANGS if lang['type'].lower() == type.value]


