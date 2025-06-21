import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

# Set up the page
st.set_page_config(page_title="🚀 Project Tracker", layout="wide")

# Style
st.markdown("""
    <style>
        .project-card {
            background-color: #f9f9f9;
            padding: 1.2rem;
            border-radius: 15px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .project-header {
            font-size: 20px;
            font-weight: bold;
        }
        .status-badge {
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .Not\ Started { background-color: #ddd; color: #444; }
        .In\ Progress { background-color: #ffdd57; color: #000; }
        .Completed { background-color: #85e085; color: #000; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'projects' not in st.session_state:
    st.session_state.projects = []

# Sidebar form
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5959/5959644.png", width=80)
    st.title("📋 Add Project")
    with st.form("project_form"):
        name = st.text_input("Project Name")
        desc = st.text_area("Description")
        start = st.date_input("Start Date", value=datetime.today())
        end = st.date_input("End Date", value=datetime.today())
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])
        submit = st.form_submit_button("Add Project")
    
    if submit:
        if name.strip() == "":
            st.error("Project name can't be empty.")
        else:
            new_id = len(st.session_state.projects) + 1
            st.session_state.projects.append({
                "ID": new_id,
                "Name": name,
                "Description": desc,
                "Start Date": start,
                "End Date": end,
                "Priority": priority,
                "Status": status
            })
            st.success(f"✅ Project '{name}' added.")

# Main display
st.title("📁 Project Dashboard")

if st.session_state.projects:
    # Filter by status
    filter_option = st.selectbox("🔍 Filter by Status", ["All", "Not Started", "In Progress", "Completed"], index=0)
    filtered = [p for p in st.session_state.projects if filter_option == "All" or p["Status"] == filter_option]

    for project in filtered:
        with st.container():
            st.markdown(f"""
                <div class="project-card">
                    <div class="project-header">{project['Name']}</div>
                    <div>{project['Description']}</div>
                    <div><b>Start:</b> {project['Start Date']} &nbsp; | &nbsp; <b>End:</b> {project['End Date']} &nbsp; | &nbsp; 
                    <b>Priority:</b> {project['Priority']}</div>
                    <div class="status-badge {project['Status']}">{project['Status']}</div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("No projects yet. Use the sidebar to add one!")

# Edit functionality
st.subheader("📝 Edit Project Status")
if st.session_state.projects:
    df = pd.DataFrame(st.session_state.projects)
    editable_df = st.data_editor(
        df[["ID", "Name", "Start Date", "End Date", "Status"]],
        column_config={"Status": st.column_config.SelectboxColumn(options=["Not Started", "In Progress", "Completed"])},
        hide_index=True,
        num_rows="dynamic"
    )
    if not editable_df.equals(df[["ID", "Name", "Start Date", "End Date", "Status"]]):
        for idx, row in editable_df.iterrows():
            st.session_state.projects[idx]["Status"] = row["Status"]
        st.rerun()

# Delete project
st.subheader("❌ Delete a Project")
delete_id = st.number_input("Enter ID to delete", min_value=1, step=1)
if st.button("Delete"):
    st.session_state.projects = [p for p in st.session_state.projects if p["ID"] != delete_id]
    st.rerun()

# Clear all
if st.button("🧹 Clear All Projects"):
    st.session_state.projects.clear()
    st.success("All projects cleared!")
    st.rerun()
