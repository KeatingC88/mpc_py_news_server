from pydantic import BaseModel

class Encrypted_Edit_Article_DTO(BaseModel):
    user_id: str
    token: str
    headline: str
    sub_headline: str
    byline: str
    image_urls: str
    body: str
    tags: str 
    source_urls: str 
    language: str
    region: str
    document_id: str