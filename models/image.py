from pydantic import BaseModel, Field

class Image(BaseModel):
    uuid: str
    name: str
    tags: str

