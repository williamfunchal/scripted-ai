import base64
from crewai.tools import BaseTool
from typing import Type
from crewai_tools.tools.serper_dev_tool.serper_dev_tool import requests
from pydantic import BaseModel, Field


class WordpressToolInput(BaseModel):
    """Input schema for Wordpress Tool."""
    title: str = Field(..., description="Post title.")
    content: str = Field(..., description="Post content.")
    status: str = Field(..., description="Post status.")
    

class WordpressTool(BaseTool):
    name: str = "Wordpress Tool"
    description: str = (
        "Publishes a post to wordpress."
    )
    args_schema: Type[BaseModel] = WordpressToolInput

    def _run(self, title: str, content: str, status: str) -> str:
        url = 'https://104.196.197.50/wp-json/wp/v2/posts'
        username = 'admin'
        password = 'ZUvg xLVp L31E icuR U5rR 50ad'
        # Encode the username and password
        auth = f"{username}:{password}"
        auth = auth.encode('utf-8')
        auth = base64.b64encode(auth).decode('utf-8')
        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json'
        }
        data = {
            'title': title,
            'content': content,
            'status': status
        }

        try:
            response = requests.post(url, json=data, headers=headers, verify=False)
            if response.status_code == 201:
                # Construct success message
                response_data = response.json()
                return f"Post created successfully: {response_data}"
            else:
                # Construct failure message
                return f"Failed to create post: {response.status_code} - {response.text}"
        except requests.RequestException as e:
            # Handle any exceptions during the HTTP request
            return f"An error occurred while making the request: {str(e)}"
