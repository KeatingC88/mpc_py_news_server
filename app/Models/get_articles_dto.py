from pydantic import BaseModel

class Get_Articles_DTO(BaseModel):
    token: str
    page_index: int