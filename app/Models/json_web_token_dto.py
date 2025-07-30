from pydantic import BaseModel

class JSON_Web_Token_DTO(BaseModel):
    token: str