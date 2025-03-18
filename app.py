from fastapi import FastAPI
from Controllers.userController import UserController
from database.db import engine, Base

app = FastAPI()

Base.metadata.create_all(engine)


@app.get("/health")
def get_health():
    return {"status": "HEALTHY"}


user_controller = UserController()

app.include_router(user_controller.router, prefix="/user", tags=["items"])
