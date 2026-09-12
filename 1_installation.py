from fastapi import FastAPI

app = FastAPI()

''' type-hints to api: this provide validation when retuning data from api: -> dict[str, str]:  '''

@app.get('/')
def index() -> dict[str, str]:
	return {'message': 'Hello World'}


@app.get('/about')
def about() -> str:
	return 'About our company which is Cool, liek JEM!'

