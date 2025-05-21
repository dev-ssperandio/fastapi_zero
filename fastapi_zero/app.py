from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi_zero.schema import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI(title='Meu Aprendizado de FastAPI')

database = []


@app.get(
    '/', status_code=HTTPStatus.OK, response_model=Message
)  # response_class=HTMLResponse
def read_root():
    return {'message': 'Hello, World!'}


@app.get('/html', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_html():
    return """
        <html>
            <head>
                <title>Olá mundo!</title>
            </head>
            <body>
                <h1 style="font-size: 200px;"> Olá mundo! </h1>
            </body>
        </html>
    """


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id

@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}

@app.get('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado!'
        )

    return database[user_id - 1]

@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail='Usuário não encontrado!'
        )
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id

@app.delete('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="Usuário não encontrado!"
        )

    return database.pop(user_id - 1)

