from fastapi import FastAPI
from Controllers.userController import UserController
from database.db import engine, Base
from dotenv import load_dotenv
from os import environ

app = FastAPI()


load_dotenv()
print(environ.get("DEBUG"))
if environ.get("DEBUG"):
    import debugpy
    print("RUNNING DEBUG MODE")
    debugpy.listen(("0.0.0.0", 5678))

Base.metadata.create_all(engine)


@app.get("/health")
def get_health():
    return {"status": "HEALTHY"}


user_controller = UserController()

app.include_router(user_controller.router, prefix="/user", tags=["items"])
