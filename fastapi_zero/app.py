from http import HTTPStatus
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi_zero.schema import Message

app = FastAPI(title="Meu Aprendizado de FastAPI")


@app.get('/', status_code=HTTPStatus.OK, response_model=Message) # response_class=HTMLResponse
def read_root():
    return {"message": "Hello, World!"}


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
