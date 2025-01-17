from scripted_ai.models.social_media_post import SocialMediaPost


class ContentOutput(BaseModel):
    article: str
    social_media_posts: List[SocialMediaPost]