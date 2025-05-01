from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    mobile: str
    firstName: str
    lastName: str = None


class User(BaseModel):
    uid: UUID
    mobile: str
    firstName: str
    lastName: str = None

class UserOutput(BaseModel):
    message: str
    status: int

class ProgramInfo(BaseModel):
    programId:str
    programTitle:str
    schedule:str
    duration:str
    manifest:str
