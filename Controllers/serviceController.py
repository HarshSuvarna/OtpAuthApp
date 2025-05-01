from fastapi import APIRouter
import subprocess
from Schemas.userSchema import ProgramInfo
from dotenv import load_dotenv
from os import environ
import requests
import xmltodict

load_dotenv()

router = APIRouter(prefix="/service")

@router.post("/record-service")
def recordDash(request:ProgramInfo):
    time = request.schedule[-9:-1]
    duration = request.duration[2:]
    # program_UID = request.programId[-8:-1]
    outputFile = f"{request.programId}-{request.schedule}".replace("/","-").replace(".", "")
    output_path = f"output/{outputFile}.mp4"
    command = f'streamlink --stdout {request.manifest} worst | ffmpeg -i - -t 30 -c copy {output_path}'
    try:
        subprocess.run(command, shell=True, check=True, executable="/bin/bash")
        message = f"{request.programTitle} has been downloaded. Started at {time} for {duration}. Thanks"
        return {"status": "success", "message":message, "file":output_path}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message":str(e)}


@router.get("/get-dvbi-services")
async def get_dbvi_services():
    try:
        # get the xml from dvbi ref containing channel/service info and manifests for each
        xml_url = f"http://{environ.get("HOST")}/{environ.get("XML_PATH")}"
        # print(xml_url)
        response_xml = requests.get(xml_url)
        parsed_json = xmltodict.parse(response_xml.content)# convert to json
        await getCSG(parsed_json) 

        return parsed_json
    except Exception as e:
        print(f"Something went wrong: {e}")


async def getCSG(service_json):
    # get the content service guide for each channel 
    for service in service_json["ServiceList"]["Service"]:
            if "ContentGuideServiceRef" in service:
                cgs_id = service["ContentGuideServiceRef"]
                xml_url = f"http://{environ.get("HOST")}/{environ.get("CGSID_PATH")}/{cgs_id}.xml"
                response_xml = requests.get(xml_url)
                parsed_json = xmltodict.parse(response_xml.content)
                service_json[cgs_id]=parsed_json