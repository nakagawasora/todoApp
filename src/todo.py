from pydantic import BaseModel, Field

class TodoResponse(BaseModel):
    id: int
    title: str
    done: bool

class TodoCreate(BaseModel):
    title: str = Field(max_length=100)