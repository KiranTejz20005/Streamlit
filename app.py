import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="🚀 Project Tracker", layout="wide")

# Custom Styles
st.markdown("""
    <style>
    .project-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .project-header {
        font-weight: 600;
        font-size: 1.2rem;
    }
    .Completed { background: #d4edda; padding: 4px 10px; border-radius: 10px; }
    .In\\ Progress { background: #fff3cd; padding: 4px 10px; border-radius: 10px; }
    .Not\\ Started { background: #f8d7da; padding: 4px 10px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# Session State Init
if 'projects' not in st.session_state:
    st.session_state.projects = []

# Sidebar Inputs
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5959/5959644.png", width=100)
    st.title("➕ Add Project")
    with st.form("project_form"):
        name = st.text_input("Project Name")
        desc = st.text_area("Description")
        start = st.date_input("Start Date", value=datetime.today())
        end = st.date_input("End Date", value=datetime.today())
        assigned_to = st.text_input("Assigned To")
        hours = st.number_input("Estimated Hours", min_value=0)
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])
        file = st.file_uploader("Attach File (optional)")
        submit = st.form_submit_button("Add Project")
        
    if submit:
        if name.strip() == "":
            st.error("Project name is required.")
        else:
            file_name = file.name if file else None
            new_id = len(st.session_state.projects) + 1
            st.session_state.projects.append({
                "ID": new_id,
                "Name": name,
                "Description": desc,
                "Start Date": start,
                "End Date": end,
                "Assigned To": assigned_to,
                "Hours": hours,
                "Priority": priority,
                "Status": status,
                "Attachment": file_name
            })
            st.success(f"✅ Project '{name}' added.")

# Main Dashboard
st.title("📁 Project Dashboard")

# Filters
col1, col2 = st.columns(2)
with col1:
    filter_status = st.selectbox("🔍 Filter by Status", ["All", "Not Started", "In Progress", "Completed"])
with col2:
    sort_by = st.selectbox("🗂️ Sort by", ["Start Date", "End Date"], index=0)

# Filter and Sort
projects_df = pd.DataFrame(st.session_state.projects)
if not projects_df.empty:
    if filter_status != "All":
        projects_df = projects_df[projects_df["Status"] == filter_status]
    projects_df = projects_df.sort_values(by=sort_by)

    # Display Projects
    for _, proj in projects_df.iterrows():
        st.markdown(f"""
            <div class="project-card">
                <div class="project-header">{proj['Name']}</div>
                <div>{proj['Description']}</div>
                <div><b>Start:</b> {proj['Start Date']} | <b>End:</b> {proj['End Date']} | <b>Hours:</b> {proj['Hours']}</div>
                <div><b>Assigned:</b> {proj['Assigned To']} | <b>Priority:</b> {proj['Priority']}</div>
                <div class="{proj['Status']}">{proj['Status']}</div>
                {"📎 Attached: " + proj['Attachment'] if proj['Attachment'] else ""}
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("No projects found.")

# Editor
st.subheader("✏️ Edit Project Status")
if not projects_df.empty:
    edit_df = st.data_editor(
        projects_df[["ID", "Name", "Status"]],
        column_config={"Status": st.column_config.SelectboxColumn(options=["Not Started", "In Progress", "Completed"])},
        hide_index=True
    )
    if not edit_df.equals(projects_df[["ID", "Name", "Status"]]):
        for i, row in edit_df.iterrows():
            st.session_state.projects[i]["Status"] = row["Status"]
        st.rerun()

# Export / Import
st.subheader("📁 Backup / Restore")
col1, col2 = st.columns(2)
with col1:
    if st.button("📤 Export to CSV"):
        df_export = pd.DataFrame(st.session_state.projects)
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "projects.csv", "text/csv")

with col2:
    uploaded_file = st.file_uploader("📥 Upload CSV", type=["csv"])
    if uploaded_file:
        new_data = pd.read_csv(uploaded_file)
        st.session_state.projects = new_data.to_dict(orient='records')
        st.success("Projects imported!")
        st.rerun()

# Delete
st.subheader("🗑️ Delete Project")
del_id = st.number_input("Enter Project ID", min_value=1, step=1)
if st.button("Delete"):
    st.session_state.projects = [p for p in st.session_state.projects if p["ID"] != del_id]
    st.success(f"Deleted project ID {del_id}")
    st.rerun()

if st.button("🧹 Clear All Projects"):
    st.session_state.projects.clear()
    st.rerun()
