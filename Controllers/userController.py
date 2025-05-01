from fastapi import APIRouter, Depends, HTTPException, status
from DI_Container import get_user_service
from Schemas.userSchema import UserBase, ProgramInfo
from Services.userService import UserService
from typing import Annotated
from helpers.mapper import get_user_model
from Schemas.userSchema import UserOutput
from dotenv import load_dotenv
from os import environ
import json
import requests
import xmltodict
import subprocess

load_dotenv()

class UserController:

    userService_dep = Annotated[UserService, Depends(get_user_service)]

    def __init__(self):
        # self.userService = userService
        self.router = APIRouter()
        self.DVBI_URL = environ.get("DVBI_URL")

        # order of endpoints matters here. Dynamically routed endpoints should be after static endpoints
        # self.router.add_api_route("/get-dvbi-services", self.get_dbvi_services, methods=["GET"])
        # self.router.add_api_route("/get-epg-data", self.get_EPG_data, methods=["GET"])
        # self.router.add_api_route("/{user_id}", self.get_user, methods=["GET"])
        # self.router.add_api_route(
        #     "/{user_id}", self.create_item, methods=["POST"], response_model=UserOutput
        # )
        # self.router.add_api_route(
        #     "/record-dash}", self.record_dash, methods=["POST"]
        # )

    async def get_user(
        self, user_id: int, userService: UserService = Depends(get_user_service)
    ):
        user = userService.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def create_item(self, user: UserBase, userService: userService_dep):
        try:
            userModel = get_user_model(user)
            createdUser = userService.create_user(userModel)
            if not createdUser:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="User not created"
                )
            return UserOutput(
                message="User Created", status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(f"Something went wrong: {e}")


    async def get_dbvi_services(self):
        try:
            # get the xml from dvbi ref containing channel/service info and manifests for each
            xml_url = f"http://{environ.get("HOST")}/{environ.get("XML_PATH")}"
            # print(xml_url)
            response_xml = requests.get(xml_url)
            parsed_json = xmltodict.parse(response_xml.content)# convert to json
            await self.getCSG(parsed_json) 

            return parsed_json
        except Exception as e:
            print(f"Something went wrong: {e}")

    async def getCSG(self, service_json):
        # get the content service guide for each channel 
        for service in service_json["ServiceList"]["Service"]:
                if "ContentGuideServiceRef" in service:
                    cgs_id = service["ContentGuideServiceRef"]
                    xml_url = f"http://{environ.get("HOST")}/{environ.get("CGSID_PATH")}/{cgs_id}.xml"
                    response_xml = requests.get(xml_url)
                    parsed_json = xmltodict.parse(response_xml.content)
                    service_json[cgs_id]=parsed_json

    # async def get_EPG_data(self):
    #     try:
    #         xml_url = f"http://{environ.get("HOST")}/{environ.get("CGSID_PATH_TEST")}"
    #         # print(xml_url)
    #         response_xml = requests.get(xml_url)
    #         parsed_json = xmltodict.parse(response_xml.content)                        
    #         return parsed_json
    #     except Exception as e:
    #         print(f"Something went wrong: {e}")

    async def record_dash(self, programInfo:ProgramInfo):
        print(programInfo)
        return "donwloaing....."
        # # Construct the streamlink command
        # command = [
        #     "streamlink",
        #     "https://akamaibroadcasteruseast.akamaized.net/cmaf/live/657078/akasource/out.mpd",
        #     "worst", 
        #     "-O"
        # ]
        
        # # Prepare the ffmpeg command to limit the duration of the stream
        # ffmpeg_command = [
        #     "ffmpeg", 
        #     "-i", "pipe:0", 
        #     "-t", str(request.duration), 
        #     "-c", "copy", 
        #     f"/home/HarshSuvarna/dvb-dash-downloads/akamaized_{request.duration}.mp4"
        # ]
        
        # # Use subprocess to run the commands
        # try:
        #     # Run streamlink and pipe the output to ffmpeg
        #     process_streamlink = subprocess.Popen(command, stdout=subprocess.PIPE)
        #     # process_ffmpeg = subprocess.Popen(ffmpeg_command, stdin=process_streamlink.stdout)

        #     # Wait for the process to complete
        #     # await asyncio.to_thread(process_ffmpeg.wait)

        #     # Close the streamlink process
        #     process_streamlink.stdout.close()
        #     process_streamlink.wait()

        #     return {"status": "success", "message": f"Recording completed for {request.duration} seconds."}
        
        # except Exception as e:
        #     return {"status": "error", "message": str(e)}

            
