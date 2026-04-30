# import streamlit as st
# import requests

# API_URL = "https://small-project-todo.onrender.com"

# st.title("Smart Task Tracker 📝")

# menu = ["Add Task", "View Tasks", "Update Task", "Delete Task"]
# choice = st.sidebar.selectbox("Menu", menu)

# if choice == "Add Task":
#     st.subheader("Add New Task")
#     title = st.text_input("Task Title")
#     description = st.text_area("Task Description")
#     priority = st.selectbox("Priority", ["Low", "Medium", "High"])

#     if st.button("Add Task"):
#         try:
#             response = requests.post(
#                 f"{API_URL}/tasks",
#                 json={
#                     "title": title,
#                     "description": description,
#                     "priority": priority
#                 }
#             )

#             data = response.json()
#             if response.status_code == 200:
#                 st.success(data.get("message", "Task added successfully!"))
#             else:
#                 st.error(data.get("detail", response.text))
#         except Exception:
#             st.error(f"Unexpected response from server: {response.text}")

# elif choice == "View Tasks":
#     st.subheader("All Tasks")
#     try:
#         response = requests.get(f"{API_URL}/tasks")
#         tasks = response.json()

#         for task in tasks:
#             status = task.get("status", "Pending")

#             if status.lower() == "completed":
#                 st.markdown(f"### ✔ {task['title']}")
#             elif status.lower() == "deleted":
#                 st.markdown(f"### 🗑 {task['title']}")
#             else:
#                 st.markdown(f"### ❌ {task['title']}")

#             st.write(f"**ID:** {task['id']}")
#             st.write(f"**Description:** {task.get('description') or 'No description'}")
#             st.write(f"**Priority:** {task.get('priority', 'Medium')}")
#             st.write(f"**Status:** {status}")
#             st.write("---")
#     except Exception as e:
#         st.error(f"Error fetching tasks: {e}")

# elif choice == "Update Task":
#     st.subheader("Mark Task as Completed")
#     task_id = st.number_input("Enter Task ID", min_value=1)

#     if st.button("Update Task"):
#         try:
#             response = requests.put(f"{API_URL}/tasks/{task_id}")
#             data = response.json()

#             if response.status_code == 200:
#                 st.success(data.get("message", "Task updated successfully!"))
#             else:
#                 st.error(data.get("detail", response.text))
#         except Exception:
#             st.error(f"Unexpected response from server: {response.text}")

# elif choice == "Delete Task":
#     st.subheader("Delete Task")
#     task_id = st.number_input("Enter Task ID to Delete", min_value=1)

#     if st.button("Delete Task"):
#         try:
#             response = requests.delete(f"{API_URL}/tasks/{task_id}")
#             data = response.json()

#             if response.status_code == 200:
#                 st.success(data.get("message", "Task deleted successfully!"))
#             else:
#                 st.error(data.get("detail", response.text))
#         except Exception:
#             st.error(f"Unexpected response from server: {response.text}")
import streamlit as st
import requests
import time

API_URL = "https://small-project-todo.onrender.com"

# ---------------- API Helper Functions ----------------
def wake_backend():
    """Wake up the Render backend if it is sleeping."""
    try:
        requests.get(f"{API_URL}/docs", timeout=30)
    except requests.exceptions.RequestException:
        pass


def make_request(method, endpoint, **kwargs):
    """Make API requests with retry logic."""
    url = f"{API_URL}{endpoint}"

    for attempt in range(3):
        try:
            response = requests.request(method, url, timeout=30, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            if attempt < 2:
                time.sleep(5)
            else:
                st.error("Backend is taking too long to start. Please refresh in a few seconds.")
                return None


# ---------------- App Setup ----------------
st.set_page_config(page_title="Smart Task Tracker", page_icon="📝", layout="centered")

with st.spinner("Starting server... Please wait a moment."):
    wake_backend()

st.title("Smart Task Tracker 📝")
st.markdown("Organize your work efficiently and never miss a task.")

menu = ["Add Task", "View Tasks", "Update Task", "Delete Task"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- Add Task ----------------
if choice == "Add Task":
    st.subheader("Add New Task")

    title = st.text_input("Task Title")
    description = st.text_area("Task Description")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])

    if st.button("Add Task"):
        if not title.strip():
            st.warning("Task title cannot be empty.")
        else:
            response = make_request(
                "POST",
                "/tasks",
                json={
                    "title": title,
                    "description": description,
                    "priority": priority,
                },
            )

            if response:
                data = response.json()
                st.success(data.get("message", "Task added successfully!"))

# ---------------- View Tasks ----------------
elif choice == "View Tasks":
    st.subheader("All Tasks")

    response = make_request("GET", "/tasks")
    if response:
        tasks = response.json()

        if not tasks:
            st.info("No tasks found.")
        else:
            for task in tasks:
                status = task.get("status", "Pending")

                if status.lower() == "completed":
                    icon = "✔"
                elif status.lower() == "deleted":
                    icon = "🗑"
                else:
                    icon = "❌"

                with st.container():
                    st.markdown(f"### {icon} {task['title']}")
                    st.write(f"**ID:** {task['id']}")
                    st.write(f"**Description:** {task.get('description') or 'No description'}")
                    st.write(f"**Priority:** {task.get('priority', 'Medium')}")
                    st.write(f"**Status:** {status}")
                    st.divider()

# ---------------- Update Task ----------------
elif choice == "Update Task":
    st.subheader("Mark Task as Completed")
    task_id = st.number_input("Enter Task ID", min_value=1, step=1)

    if st.button("Update Task"):
        response = make_request("PUT", f"/tasks/{task_id}")

        if response:
            data = response.json()
            st.success(data.get("message", "Task updated successfully!"))

# ---------------- Delete Task ----------------
elif choice == "Delete Task":
    st.subheader("Delete Task")
    task_id = st.number_input("Enter Task ID to Delete", min_value=1, step=1)

    if st.button("Delete Task"):
        response = make_request("DELETE", f"/tasks/{task_id}")

        if response:
            data = response.json()
            st.success(data.get("message", "Task deleted successfully!"))