from fastapi import Depends
from sqlalchemy.orm import Session
from database.db import get_db
from Services.userService import UserService



def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)
