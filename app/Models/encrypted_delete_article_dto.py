from pydantic import BaseModel

class Encrypted_Delete_Article_DTO(BaseModel):
    token: str
    article_id: str