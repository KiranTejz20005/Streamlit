import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state if not already initialized
if 'projects' not in st.session_state:
    st.session_state.projects = []

# Page configuration
st.set_page_config(page_title="Project Tracker", layout="wide")
st.title("📂 Project Tracker")

# Sidebar - Input form
with st.sidebar.form(key='project_form'):
    st.header("➕ Add New Project")
    project_name = st.text_input("Project Name")
    project_desc = st.text_area("Description")
    start_date = st.date_input("Start Date", value=datetime.today())
    end_date = st.date_input("End Date", value=datetime.today())
    status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])
    submit_button = st.form_submit_button(label='Add Project')

    if submit_button:
        if project_name.strip() == "":
            st.error("Project name cannot be empty.")
        else:
            project_id = len(st.session_state.projects) + 1
            st.session_state.projects.append({
                "ID": project_id,
                "Name": project_name,
                "Description": project_desc,
                "Start Date": start_date,
                "End Date": end_date,
                "Status": status
            })
            st.success(f"✅ Project '{project_name}' added successfully!")

# Main area - Display and edit projects
if st.session_state.projects:
    st.subheader("📋 Manage Projects")

    # Convert list of dicts to DataFrame
    df = pd.DataFrame(st.session_state.projects)

    # Use data_editor to allow editing only the 'Status' column
    edited_df = st.data_editor(
        df[["ID", "Name", "Description", "Start Date", "End Date", "Status"]],
        column_config={
            "Status": st.column_config.SelectboxColumn(
                options=["Not Started", "In Progress", "Completed"],
                required=True
            )
        },
        hide_index=True,
        num_rows="dynamic"
    )

    # Update session state based on edited DataFrame
    if not edited_df.equals(df):
        # Update the session state projects list
        updated_projects = edited_df.to_dict(orient='records')
        st.session_state.projects = updated_projects
        st.rerun()

    # Optional: Add delete buttons for each project
    st.subheader("🗑️ Delete Projects")
    delete_id = st.number_input("Enter Project ID to delete", min_value=1, step=1)
    if st.button("Delete Project"):
        st.session_state.projects = [p for p in st.session_state.projects if p['ID'] != delete_id]
        st.rerun()
else:
    st.info("No projects added yet. Use the sidebar to add one.")

# Optional: Clear all projects button
if st.button("🗑️ Clear All Projects"):
    st.session_state.projects = []
    st.rerun()