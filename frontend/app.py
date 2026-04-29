import streamlit as st
import requests

# API_URL = "http://127.0.0.1:8000"
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
        response = requests.post(
            f"{API_URL}/tasks",
            json={
                "title": title,
                "description": description,
                "priority": priority
            }
        )
        st.success(response.json()["message"])

elif choice == "View Tasks":
    st.subheader("All Tasks")
    response = requests.get(f"{API_URL}/tasks")
    tasks = response.json()

    for task in tasks:
        status = task["status"]

        # 🔥 Add green tick if completed
        if status.lower() == "completed":
            st.markdown(
                f"""
                ### ✔ {task['title']}
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                ### ❌ {task['title']}
                """,
                unsafe_allow_html=True
            )

        st.write(f"**ID:** {task['id']}")
        st.write(f"**Description:** {task.get('description', 'No description')}")
        st.write(f"**Priority:** {task.get('priority', 'Medium')}")
        st.write(f"**Status:** {status}")
        st.write("---")

elif choice == "Update Task":
    st.subheader("Mark Task as Completed")
    task_id = st.number_input("Enter Task ID", min_value=1)

    if st.button("Update Task"):
        response = requests.put(f"{API_URL}/tasks/{task_id}")
        st.success(response.json()["message"])

elif choice == "Delete Task":
    st.subheader("Delete Task")
    task_id = st.number_input("Enter Task ID to Delete", min_value=1)

    if st.button("Delete Task"):
        response = requests.delete(f"{API_URL}/tasks/{task_id}")
        st.success(response.json()["message"])