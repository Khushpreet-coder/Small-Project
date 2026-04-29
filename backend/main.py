from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import conn, cursor

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str | None = None
    priority: str = "Medium"

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete FastAPI assignment",
                "description": "Submit the To-Do project on Educollab",
                "priority": "High"
            }
        }

@app.get("/")
def home():
    return {"message": "To-Do API is running"}

@app.post("/tasks")
def add_task(task: Task):
    query = """
    INSERT INTO tasks (title, description, priority)
    VALUES (%s, %s, %s)
    """
    cursor.execute(
        query,
        (task.title, task.description, task.priority)
    )
    conn.commit()
    return {"message": "Task added successfully"}

@app.get("/tasks")
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()

@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        "UPDATE tasks SET status = 'Completed' WHERE id = %s",
        (task_id,)
    )
    conn.commit()
    return {"message": "Task marked as completed"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        "UPDATE tasks SET status = 'Deleted' WHERE id = %s",
        (task_id,)
    )
    conn.commit()
    return {"message": "Task marked as deleted"}