from pydantic import BaseModel, Field

# フロントエンドに返すTODOの型 (TypeScriptの interface Todo に相当)
class TodoResponse(BaseModel):
    id: int
    title: str
    done: bool

# TODO作成時にフロントエンドから受け取るデータの型 (TypeScriptの Omit<Todo, 'id' | 'done'> 等に相当)
class TodoCreate(BaseModel):
    title: str = Field(max_length=100)