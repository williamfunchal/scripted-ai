from pydantic import BaseModel


class SocialMediaPost(BaseModel):
    platform: str
    content: str