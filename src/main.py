from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from todo import TodoCreate, TodoResponse
from db import get_db, init_db

init_db()

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/todos", response_model=list[TodoResponse])
async def get_todos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM todos ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [{"id": row["id"], "title": row["title"], "done": bool(row["done"])} for row in rows]

@app.post("/api/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    clean_title = todo.title.strip()
    if not clean_title:
        raise HTTPException(status_code=400, detail="タイトルは必須です")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (title, done) VALUES (?, ?)", (clean_title, False))
    conn.commit()
    todo_id = cursor.lastrowid
    conn.close()
    
    return TodoResponse(id=todo_id, title=clean_title, done=False)

@app.put("/api/todos/{todo_id}", response_model=TodoResponse)
async def toggle_todo(todo_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, done FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="見つかりません")
    
    new_done = not bool(row["done"])
    cursor.execute("UPDATE todos SET done = ? WHERE id = ?", (new_done, todo_id))
    conn.commit()
    conn.close()
    
    return TodoResponse(id=row["id"], title=row["title"], done=new_done)

@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    
    if changes == 0:
        raise HTTPException(status_code=404, detail="見つかりません")
    return {"message": "削除しました"}