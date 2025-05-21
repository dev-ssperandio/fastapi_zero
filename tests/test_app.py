from http import HTTPStatus


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

def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'BADI',
                'email': 'badi@example.com',
            },
        ]
    }

def teste_get_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'BADI',
        'email': 'badi@example.com',
        'id': 1,
    }

def teste_get_user_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "detail": "Usuário não encontrado!"
    }

def test_update_user(client):
    response = client.put(
        '/users/1', 
        json={
            'username': 'VITA',
            'email': 'vita@example.com',
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
        "detail": "Usuário não encontrado!"
    }

def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'VITA',
        'email': 'vita@example.com',
        'id': 1
    }

def test_delete_user_not_found(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "detail": "Usuário não encontrado!"
    }
