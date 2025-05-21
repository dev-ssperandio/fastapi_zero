from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


# Exemplo de comunicação entre cliente e servidor através de um JSON

# {
#     'username': "BADI",
#     'email': "badi@email.com",
#     'password': "BADI123"
# }


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int


class UserDB(UserSchema):
    id: int

class UserList(BaseModel):
    users: list[UserPublic]
