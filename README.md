# ToDo API 

This project contains a REST API used for managing ToDos.

## Pre-requirements 

### .env file 
Before installing dependencies a ``.env`` file has to be prepared 
- Required env variables:
  - SECRET_KEY - Used for creating access tokens 

For demo purposes the provided ``.env.example`` can be used.

Therefore use command: ``cp .env.example .env``

### Poetry
Install poetry if not already installed: [installation guide ](https://python-poetry.org/docs/#installation)

## Running the API

- Dependencies are managed using poetry. To install all packages run:
  - ``poetry install``
- To run the API:
  - ``poetry run fastapi dev app/main.py``
  - Working directory should be /todo-api
  
To see all given endpoints visit: http://127.0.0.1:8000/docs

In order to use ToDo endpoints you first have to create a user
and authorize using the users credentials.

## Notes

- OAuth2 is used to keep the routes secure