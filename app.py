from fastapi import FastAPI
from Controllers.userController import UserController
from database.db import engine, Base
from dotenv import load_dotenv
from os import environ
from fastapi.middleware.cors import CORSMiddleware
from Schemas.userSchema import ProgramInfo
import subprocess



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
    time = request.schedule[-9:-1]
    duration = request.duration[2:]
    output_path = "output/test4.mp4"
    command = f'streamlink --stdout "https://akamaibroadcasteruseast.akamaized.net/cmaf/live/657078/akasource/out.mpd" worst | ffmpeg -i - -t 30 -c copy {output_path}'
    try:
        subprocess.run(command, shell=True, check=True, executable="/bin/bash")
        message = f"{request.programTitle} has been downloaded. Started at {time} for {duration}. Thanks"
        return {"status": "success", "message":message, "file":output_path}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message":str(e)}

user_controller = UserController()

app.include_router(user_controller.router, prefix="/user", tags=["items"])
