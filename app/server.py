import os
import sys
import json
import uvicorn
from pathlib import Path
from loguru import logger
from fastapi import FastAPI
from starlette.responses import FileResponse

class Server:
    def __init__(self):
        self.app = FastAPI(title="ims", description="Generates IMS Radar and Sat images", version='1.0.0',  contact={"name": "Tomer Klein", "email": "tomer.klein@gmail.com", "url": "https://github.com/t0mer/Wazy"})

        @self.app.get("/me-sat")
        async def get_image():
            image_path = Path("images/me_sat.gif")
            print(image_path)
            if not image_path.is_file():
                return {"error": "Image not found on the server"}
            return FileResponse(image_path)

        @self.app.get("/eu-sat")
        async def get_image():
            image_path = Path("images/eu_sat.gif")
            if not image_path.is_file():
                return {"error": "Image not found on the server"}
            return FileResponse(image_path)

        @self.app.get("/radar")
        async def get_image():
            image_path = Path("images/radar.gif")
            if not image_path.is_file():
                return {"error": "Image not found on the server"}
            return FileResponse(image_path)

    def start(self):
        logger.info("Starting the server")
        uvicorn.run(self.app, host="0.0.0.0", port=8081)

server = Server()
server.start()