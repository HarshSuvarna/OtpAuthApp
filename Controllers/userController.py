from fastapi import APIRouter, Depends, HTTPException, status
from DI_Container import get_user_service
from Schemas.userSchema import UserBase
from Services.userService import UserService
from typing import Annotated
from helpers.mapper import get_user_model
from Schemas.userSchema import UserOutput
from dotenv import load_dotenv
from os import environ
import json
import requests
import xmltodict
load_dotenv()

class UserController:

    userService_dep = Annotated[UserService, Depends(get_user_service)]

    def __init__(self):
        # self.userService = userService
        self.router = APIRouter()
        self.DVBI_URL = environ.get("DVBI_URL")

        # order of endpoints matters here. Dynamically routed endpoints should be after static endpoints
        self.router.add_api_route("/get-dvbi-services", self.get_dbvi_services, methods=["GET"])
        self.router.add_api_route("/get-epg-data", self.get_EPG_data, methods=["GET"])
        self.router.add_api_route("/{user_id}", self.get_user, methods=["GET"])
        self.router.add_api_route(
            "/{user_id}", self.create_item, methods=["POST"], response_model=UserOutput
        )

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
            xml_url = f"http://{environ.get("HOST")}/{environ.get("XML_PATH")}"
            # print(xml_url)
            response_xml = requests.get(xml_url)
            parsed_json = xmltodict.parse(response_xml.content)
            return parsed_json
        except Exception as e:
            print(f"Something went wrong: {e}")

    async def get_EPG_data(self):
        try:
            xml_url = f"http://{environ.get("HOST")}/{environ.get("CGSIG_PATH")}"
            # print(xml_url)
            response_xml = requests.get(xml_url)
            parsed_json = xmltodict.parse(response_xml.content)
            return parsed_json
        except Exception as e:
            print(f"Something went wrong: {e}")
