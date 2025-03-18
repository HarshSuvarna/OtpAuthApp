from sqlalchemy.orm import Session
from models.userModel import User
from Schemas.userSchema import UserOutput


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, id: int):
        return self.db.query(User).filter(User.uid == id).first()

    def create_user(self, user: User) -> UserOutput:
        self.db.add(user)
        self.db.commit()
        # return "FINE"
        return user
