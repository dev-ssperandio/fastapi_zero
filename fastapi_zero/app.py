from http import HTTPStatus
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schema import Message, UserList, UserPublic, UserSchema

app = FastAPI(title='Meu Aprendizado de FastAPI')


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
def create_user(user: UserSchema, session: Session=Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user: 
        if db_user.username == user.username:
            raise HTTPException(
                detail='Username já existe',
                status_code=HTTPStatus.CONFLICT
            )
        elif db_user.email == user.email:
            raise HTTPException(
                detail='E-mail já existe',
                status_code=HTTPStatus.CONFLICT
            )
        
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(limit=10, offset=0, session: Session=Depends(get_session)):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}

@app.get('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user(user_id: int, session: Session=Depends(get_session)):
    user = session.scalar(select(User).where(User.id == user_id))

    if user_id < 1 or user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado'
        )

    return user

@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    
    if user_db is None:
        raise HTTPException(
            detail='Usuário não encontrado',
            status_code=HTTPStatus.NOT_FOUND
        )
    
    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db  
    except IntegrityError:
        raise HTTPException(
            detail='Username ou Email já existe',
            status_code=HTTPStatus.CONFLICT
        )

@app.delete('/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    
    if user_db is None:
        raise HTTPException(
            detail='Usuário não encontrado',
            status_code=HTTPStatus.NOT_FOUND
        )

    session.delete(user_db)
    session.commit()

    return {'message': 'Usuário deletado'}
    