from pydantic import BaseModel, Field, ConfigDict


class SBookAdd(BaseModel):
    title: str
    author: str
    year: int
    pages: int = Field(..., gt=10)
    is_read: bool = False


class SBook(SBookAdd):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
