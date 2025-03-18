from Schemas.userSchema import UserBase
from models.userModel import User
from uuid import uuid4
from datetime import datetime


def get_user_model(user: UserBase) -> User:

    return User(**user.model_dump(), uid=uuid4(), creationTime=datetime.now())
