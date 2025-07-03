from fastapi import FastAPI

from fastapi_zero.routers import auth, users

app = FastAPI(title='Meu Aprendizado de FastAPI')

app.include_router(auth.router)
app.include_router(users.router)
