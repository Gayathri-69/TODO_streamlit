import streamlit as st
from datetime import date

# Title of the application
st.title("MY TODO APPLICATION")

# Initialize the session state
if 'dummy_data' not in st.session_state:
    st.session_state['dummy_data'] = []
if 'completed_tasks' not in st.session_state:
    st.session_state['completed_tasks'] = set()

dummy_data = st.session_state['dummy_data']

def checkbox_container(data):
    new_task = st.text_input('Enter task')
    due_date = st.date_input(label="Due Date", value=date.today())
    
    cols = st.columns(10)
    st.subheader("My Works")
    if cols[0].button('Add'):
        if new_task:  # Only add non-empty tasks
            dummy_data.append((new_task, due_date))  # Store task and due date as a tuple
    
    for idx, (task, _) in enumerate(data):
        key = f'dynamic_checkbox_{idx}'
        
        # Check if the task is already completed
        if key in st.session_state['completed_tasks']:
            checked = True
        else:
            checked = False
        
        # Display the checkbox and task text
        checkbox_col, task_col, due_date_col = st.columns([1, 8, 1])
        if checkbox_col.checkbox('', key=key, value=checked):
            st.session_state['completed_tasks'].add(key)
        else:
            st.session_state['completed_tasks'].discard(key)
        
        with task_col:
            # Display the task with strike-through if it's completed
            if key in st.session_state['completed_tasks']:
                st.markdown(f'<span style="text-decoration: line-through; font-size: 16px;">{task}</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span style="font-size: 16px;">{task}</span>', unsafe_allow_html=True)
        
        with due_date_col:
            # Display the due date next to the checkbox with adjusted font size
            st.markdown(f'<span style="font-size: 14px;">Due Date: {due_date}</span>', unsafe_allow_html=True)

def get_selected_tasks():
    selected_tasks = []
    for key in st.session_state['completed_tasks']:
        idx = int(key.split('_')[2])
        selected_tasks.append(st.session_state['dummy_data'][idx])
    return selected_tasks

checkbox_container(dummy_data)

st.subheader('Tasks Completed')
completed_tasks = get_selected_tasks()

# Display new_data and due_date in a table below
if completed_tasks:
    # Rename the columns as Tasks and Due Date
    renamed_tasks = [{'Tasks': task[0], 'Due Date': task[1]} for task in completed_tasks]
    st.table(renamed_tasks)
else:
    st.write("No tasks completed yet.")
