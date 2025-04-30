from fastapi import FastAPI
from Controllers.userController import UserController
from database.db import engine, Base
from dotenv import load_dotenv
from os import environ
from fastapi.middleware.cors import CORSMiddleware
from Schemas.userSchema import ProgramInfo




app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], 
                   allow_credentials=True, allow_methods=["*"], 
                   allow_headers=["*"])

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




@app.post("/record-dash")
def recordDash(request:ProgramInfo):
    print(request)
    time = request.schedule[-9:-1]
    duration = request.duration[2:]
    return f"{request.programTitle} will start recording at {time} for {duration}. Thanks"

user_controller = UserController()

app.include_router(user_controller.router, prefix="/user", tags=["items"])
