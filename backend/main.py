# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from database import conn, cursor
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # For production, you can restrict this later
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class Task(BaseModel):
#     title: str
#     description: str | None = None
#     priority: str = "Medium"

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "title": "Complete FastAPI assignment",
#                 "description": "Submit the To-Do project on Educollab",
#                 "priority": "High"
#             }
#         }

# @app.get("/")
# def home():
#     return {"message": "To-Do API is running"}

# @app.post("/tasks")
# def add_task(task: Task):
#     query = """
#     INSERT INTO tasks (title, description, priority)
#     VALUES (%s, %s, %s)
#     """
#     cursor.execute(
#         query,
#         (task.title, task.description, task.priority)
#     )
#     conn.commit()
#     return {"message": "Task added successfully"}

# @app.get("/tasks")
# def get_tasks():
#     cursor.execute("SELECT * FROM tasks")
#     return cursor.fetchall()

# @app.put("/tasks/{task_id}")
# def update_task(task_id: int):
#     cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
#     task = cursor.fetchone()

#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")

#     cursor.execute(
#         "UPDATE tasks SET status = 'Completed' WHERE id = %s",
#         (task_id,)
#     )
#     conn.commit()
#     return {"message": "Task marked as completed"}

# @app.delete("/tasks/{task_id}")
# def delete_task(task_id: int):
#     cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
#     task = cursor.fetchone()

#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")

#     cursor.execute(
#         "UPDATE tasks SET status = 'Deleted' WHERE id = %s",
#         (task_id,)
#     )
#     conn.commit()
#     return {"message": "Task marked as deleted"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MODEL ----------------
class Task(BaseModel):
    title: str
    description: str | None = None
    priority: str = "Medium"

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "To-Do API is running"}

# ---------------- CREATE TASK ----------------
@app.post("/tasks")
def add_task(task: Task):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO tasks (title, description, priority) VALUES (%s, %s, %s)",
            (task.title, task.description, task.priority)
        )
        conn.commit()

        return {"message": "Task added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

# ---------------- GET TASKS ----------------
@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()

        return [
            {
                "id": r[0],
                "title": r[1],
                "description": r[2],
                "priority": r[3],
                "status": r[4],
            }
            for r in rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

# ---------------- UPDATE TASK ----------------
@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Task not found")

        cursor.execute(
            "UPDATE tasks SET status = 'Completed' WHERE id = %s",
            (task_id,)
        )
        conn.commit()

        return {"message": "Task marked as completed"}

    finally:
        cursor.close()
        conn.close()

# ---------------- DELETE TASK ----------------
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Task not found")

        cursor.execute(
            "UPDATE tasks SET status = 'Deleted' WHERE id = %s",
            (task_id,)
        )
        conn.commit()

        return {"message": "Task marked as deleted"}

    finally:
        cursor.close()
        conn.close()