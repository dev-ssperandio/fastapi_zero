from http import HTTPStatus

from fastapi_zero.schema import UserPublic


def test_root_deve_retornar_ola_mundo(client):
    response = client.get('/')

    assert response.json() == {'message': 'Hello, World!'}
    assert response.status_code == HTTPStatus.OK


def test_read_html_deve_retornar_um_html(client):
    # Act
    response = client.get('/html')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.headers['content-type'] == 'text/html; charset=utf-8'


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'BADI',
            'email': 'badi@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'BADI',
        'email': 'badi@example.com',
    }

def test_create_user_username_already_exists(client):
    client.post(
        '/users/',
        json={
            'username': 'BADI',
            'email': 'badi@example.com',
            'password': 'secret'
        }
    )

    response = client.post(
        '/users/',
        json={
            'username': 'BADI',
            'email': 'outherbadi@example.com',
            'password': 'secret'
        }
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username já existe'}


def test_create_user_email_already_exists(client):
    client.post(
        '/users/',
        json={
            'username': 'BADI',
            'email': 'badi@example.com',
            'password': 'secret'
        }
    )

    response = client.post(
        '/users/',
        json={
            'username': 'OUTHERBADI',
            'email': 'badi@example.com',
            'password': 'secret'
        }
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'E-mail já existe'}




def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': []
    }

def test_read_users_with_users(client, user):

    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [user_schema]
    }

def teste_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema
    

def teste_read_user_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "detail": "Usuário não encontrado"
    }

def test_update_user(client, user):
    response = client.put(
        f'/users/{user.id}', 
        json={
            'username': 'teste_updt',
            'email': 'teste_updt@example.com',
            'password': 'secret'
        }
    )

    assert response.status_code == HTTPStatus.OK    
    assert response.json() == {
        'username': 'VITA',
        'email': 'vita@example.com',
        'id': 1
    }

def test_update_user_not_found(client):
    response = client.put(
        '/users/3',
        json={
            'username': 'VITA',
            'email': 'vita@example.com',
            'password': 'secret'
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND 
    assert response.json() == {
        "detail": "Usuário não encontrado"
    }

def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário deletado'}

def test_delete_user_not_found(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "detail": 'Usuário não encontrado'
    }


def test_update_integrity_error(client, user):
    client.post(
        '/users/',
        json={
            'username': 'BADI',
            'email': 'badi@example.com',
            'password': 'secret'
        }
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'BADI',
            'email': 'test@example.com',
            'password': 'secret'
        }
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username ou Email já existe'}