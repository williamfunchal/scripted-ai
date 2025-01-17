
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests

class ImageDownloaderInput(BaseModel):
    url: str = Field(..., description="The URL of the image to stream.")

class ImageDownloaderTool(BaseTool):
    name: str = "Image Downloader"
    description: str = "Streams an image from or to a given URL."
    args_schema: Type[BaseModel] = ImageDownloaderInput
    
    def _run(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        with open("header.png", "wb") as f:
            f.write(response.content)
        
        