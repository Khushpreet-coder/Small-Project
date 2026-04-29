import streamlit as st
import requests

API_URL = "https://small-project-todo.onrender.com"

st.title("Smart Task Tracker 📝")

menu = ["Add Task", "View Tasks", "Update Task", "Delete Task"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Task":
    st.subheader("Add New Task")
    title = st.text_input("Task Title")
    description = st.text_area("Task Description")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])

    if st.button("Add Task"):
        try:
            response = requests.post(
                f"{API_URL}/tasks",
                json={
                    "title": title,
                    "description": description,
                    "priority": priority
                }
            )

            data = response.json()
            if response.status_code == 200:
                st.success(data.get("message", "Task added successfully!"))
            else:
                st.error(data.get("detail", response.text))
        except Exception:
            st.error(f"Unexpected response from server: {response.text}")

elif choice == "View Tasks":
    st.subheader("All Tasks")
    try:
        response = requests.get(f"{API_URL}/tasks")
        tasks = response.json()

        for task in tasks:
            status = task.get("status", "Pending")

            if status.lower() == "completed":
                st.markdown(f"### ✔ {task['title']}")
            elif status.lower() == "deleted":
                st.markdown(f"### 🗑 {task['title']}")
            else:
                st.markdown(f"### ❌ {task['title']}")

            st.write(f"**ID:** {task['id']}")
            st.write(f"**Description:** {task.get('description') or 'No description'}")
            st.write(f"**Priority:** {task.get('priority', 'Medium')}")
            st.write(f"**Status:** {status}")
            st.write("---")
    except Exception as e:
        st.error(f"Error fetching tasks: {e}")

elif choice == "Update Task":
    st.subheader("Mark Task as Completed")
    task_id = st.number_input("Enter Task ID", min_value=1)

    if st.button("Update Task"):
        try:
            response = requests.put(f"{API_URL}/tasks/{task_id}")
            data = response.json()

            if response.status_code == 200:
                st.success(data.get("message", "Task updated successfully!"))
            else:
                st.error(data.get("detail", response.text))
        except Exception:
            st.error(f"Unexpected response from server: {response.text}")

elif choice == "Delete Task":
    st.subheader("Delete Task")
    task_id = st.number_input("Enter Task ID to Delete", min_value=1)

    if st.button("Delete Task"):
        try:
            response = requests.delete(f"{API_URL}/tasks/{task_id}")
            data = response.json()

            if response.status_code == 200:
                st.success(data.get("message", "Task deleted successfully!"))
            else:
                st.error(data.get("detail", response.text))
        except Exception:
            st.error(f"Unexpected response from server: {response.text}")