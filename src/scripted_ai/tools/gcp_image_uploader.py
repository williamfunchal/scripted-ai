from typing import Type
import uuid
from google.cloud import storage
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class GCPImageUploaderInput(BaseModel):
    image_path: str = Field(..., description="The path to the image file to upload.")
    # bucket_name: str = Field(..., description="The name of the GCP bucket to upload the image to.")
    # object_name: str = Field(..., description="The name of the object to upload the image to.")

class GCPImageUploaderTool(BaseTool):
    name: str = "GCPImageUploaderTool"
    description: str = "Uploads an image to GCP and returns the URL of the uploaded image."
    args_schema: Type[BaseModel] = GCPImageUploaderInput
    
    def _run(self, image_path: str):
        # Upload the image to GCP
        client = storage.Client.from_service_account_json("credentials.json")
        bucket = client.get_bucket("images_scripted_bucket")
        # UUID based object name
        img_blob_name = "image_" + str(uuid.uuid4()) + ".png"
        blob = bucket.blob(img_blob_name)
        blob.upload_from_filename("./" + image_path)
        return f"https://storage.googleapis.com/{bucket.name}/{img_blob_name}"