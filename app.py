"""
ResourceFlow - The Institutional Event Governance Platform
----------------------------------------------------------
A single-file Streamlit application for managing institutional events,
resources, and approval workflows with conflict detection.

Author: Antigravity (Google DeepMind)
Date: 2024
"""
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# --------------------------------------------------------------------------------
# 0. UI Configuration & Custom CSS
# --------------------------------------------------------------------------------
st.set_page_config(page_title="ResourceFlow", layout="wide", page_icon="🏛️")

# --------------------------------------------------------------------------------
# 0. UI Configuration & Ultra-Premium Custom CSS
# --------------------------------------------------------------------------------
st.markdown("""
    <style>
        /* Import Modern Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        /* Global Reset & Typography */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #e0e0e0;
        }

        /* Animated Deep Space Background */
        .stApp {
            background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Sidebar Glassmorphism */
        [data-testid="stSidebar"] {
            background: rgba(15, 12, 41, 0.85);
            backdrop-filter: blur(12px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 5px 0 25px rgba(0,0,0,0.3);
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.4);
        }

        /* Primary Headings */
        h1, h2, h3 {
            color: #ffffff !important;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        h1 {
            background: linear-gradient(90deg, #ff8a00, #e52e71);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Inputs & Selectboxes - Neumorphic Dark */
        .stTextInput > div > div > input, 
        .stSelectbox > div > div > div, 
        .stDateInput > div > div > input,
        .stTimeInput > div > div > input {
            background-color: rgba(255, 255, 255, 0.07);
            color: #fff;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 10px;
            transition: all 0.3s ease;
        }
        .stTextInput > div > div > input:focus, 
        .stSelectbox > div > div > div:focus {
            border-color: #e52e71;
            box-shadow: 0 0 10px rgba(229, 46, 113, 0.3);
            background-color: rgba(255, 255, 255, 0.1);
        }

        /* Buttons - Glowing Gradient */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 12px 28px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4);
        }
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 8px 25px rgba(118, 75, 162, 0.6);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }

        /* Cards / Expanders */
        div[data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            margin-bottom: 10px;
            transition: all 0.2s ease;
        }
        div[data-testid="stExpander"]:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
        }

        /* DataTables */
        [data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            overflow: hidden;
        }
        
        /* Metric Cards */
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
            color: #e52e71 !important;
        }

        /* Remove Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Success/Error/Info Messages */
        .stAlert {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------------
# 1. Session State Initialization (Simulated Database)
# --------------------------------------------------------------------------------
def init_data():
    if 'initialized' not in st.session_state:
        # Dummy Venues
        st.session_state['venues'] = {
            'Main Auditorium': 500,
            'Conference Room A': 50,
            'Computer Lab 1': 30
        }
        
        # Dummy Departments
        st.session_state['departments'] = ['CSE', 'ECE', 'MECH']

        # Dummy Equipment
        st.session_state['equipment'] = ['Projector', 'Sound System', 'Whiteboard', 'Webcam']
        
        # Dummy Events
        # Status Workflow: Pending -> HOD Approved -> Dean Approved -> Final Approved
        st.session_state['events'] = [
            {
                'id': 1,
                'name': 'AI Workshop',
                'dept': 'CSE',
                'coordinator': 'Prof. Alan',
                'venue': 'Conference Room A',
                'start_time': datetime.datetime.now() + datetime.timedelta(days=1, hours=2), # Tomorrow 2 hours from now
                'end_time': datetime.datetime.now() + datetime.timedelta(days=1, hours=4),
                'equipment': ['Projector'],
                'status': 'Pending'
            },
            {
                'id': 2,
                'name': 'Robotics Hackathon',
                'dept': 'ECE',
                'coordinator': 'Dr. Tesla',
                'venue': 'Main Auditorium',
                'start_time': datetime.datetime.now() + datetime.timedelta(days=2, hours=10),
                'end_time': datetime.datetime.now() + datetime.timedelta(days=2, hours=16),
                'equipment': ['Sound System', 'Projector'],
                'status': 'HOD Approved'
            },
            {
                'id': 3,
                'name': 'Freshers Welcome',
                'dept': 'MECH',
                'coordinator': 'Mr. Gear',
                'venue': 'Main Auditorium',
                'start_time': datetime.datetime.now() - datetime.timedelta(days=1, hours=2), # Yesterday (Completed)
                'end_time': datetime.datetime.now() - datetime.timedelta(days=1),
                'equipment': ['Sound System'],
                'status': 'Completed'
            },
             {
                'id': 4,
                'name': 'Guest Lecture',
                'dept': 'CSE',
                'coordinator': 'Prof. Knuth',
                'venue': 'Conference Room A',
                'start_time': datetime.datetime.now() + datetime.timedelta(days=3, hours=9),
                'end_time': datetime.datetime.now() + datetime.timedelta(days=3, hours=11),
                'equipment': ['Projector', 'Webcam'],
                'status': 'Final Approved'
            }
        ]
        st.session_state['initialized'] = True

init_data()

# --------------------------------------------------------------------------------
# 2. Conflict Detection Engine (CRITICAL)
# --------------------------------------------------------------------------------
def check_availability(start_time, end_time, venue, current_event_id=None):
    """
    Checks if the venue is available for the given time slot.
    Returns: (is_available: bool, message: str)
    """
    for event in st.session_state['events']:
        # Skip checking against itself if editing (not implemented fully here but good practice)
        if current_event_id and event['id'] == current_event_id:
            continue
            
        # Only check active events (not rejected or completed)
        if event['status'] in ['Rejected', 'Completed']:
            continue

        if event['venue'] == venue:
            # Overlap Logic:
            # (StartA < EndB) and (EndA > StartB)
            # Reference: Standard interval overlap formula
            if start_time < event['end_time'] and end_time > event['start_time']:
                return False, f"Conflict: {venue} is booked by Dept {event['dept']} for '{event['name']}' from {event['start_time'].strftime('%H:%M')} to {event['end_time'].strftime('%H:%M')}."
    
    return True, "Venue Available"

# --------------------------------------------------------------------------------
# 3. Sidebar: Role-Based Access Control (RBAC)
# --------------------------------------------------------------------------------
st.set_page_config(page_title="InstiEvent Manager", layout="wide")

st.sidebar.title("🔐 Login / Role")
role = st.sidebar.selectbox(
    "Select Your Role",
    ["Event Coordinator", "HOD", "Dean", "Institutional Head", "Admin"]
)

# Department Context for HOD/Coordinator (Simulated Login)
if role in ["Event Coordinator", "HOD"]:
    user_dept = st.sidebar.selectbox("Select Your Department", st.session_state['departments'])
else:
    user_dept = "ALL"

st.sidebar.markdown("---")
st.sidebar.info(f"Logged in as: **{role}**")
if user_dept != "ALL":
    st.sidebar.info(f"Department: **{user_dept}**")

# --------------------------------------------------------------------------------
# 4. Main Views based on Role
# --------------------------------------------------------------------------------

st.title("ResourceFlow - The Institutional Event Governance Platform")

# --- VIEW: Event Coordinator ----------------------------------------------------
if role == "Event Coordinator":
    st.header(f"📅 New Event Request ({user_dept})")
    
    with st.form("event_request_form"):
        col1, col2 = st.columns(2)
        with col1:
            evt_name = st.text_input("Event Name")
            evt_venue = st.selectbox("Venue", list(st.session_state['venues'].keys()))
            evt_equip = st.multiselect("Equipment Needed", st.session_state['equipment'])
        with col2:
            d = st.date_input("Date", datetime.date.today() + datetime.timedelta(days=1))
            t_start = st.time_input("Start Time", datetime.time(9, 0))
            t_end = st.time_input("End Time", datetime.time(11, 0))

        submit = st.form_submit_button("Check Availability & Submit")

    if submit:
        # Combine date and time
        start_dt = datetime.datetime.combine(d, t_start)
        end_dt = datetime.datetime.combine(d, t_end)

        if end_dt <= start_dt:
            st.error("End time must be after start time.")
        else:
            # CALL CONFLICT DETECTION ENGINE
            is_avail, msg = check_availability(start_dt, end_dt, evt_venue)
            
            if not is_avail:
                st.error(f"❌ {msg}")
            else:
                # Create Event
                new_id = max([e['id'] for e in st.session_state['events']]) + 1 if st.session_state['events'] else 1
                new_event = {
                    'id': new_id,
                    'name': evt_name,
                    'dept': user_dept,
                    'coordinator': 'Current User', # In a real app, this would be the logged-in user
                    'venue': evt_venue,
                    'start_time': start_dt,
                    'end_time': end_dt,
                    'equipment': evt_equip,
                    'status': 'Pending'
                }
                st.session_state['events'].append(new_event)
                st.success(f"✅ Event '{evt_name}' requested successfully! Status: Pending")

    st.subheader("My Department Events & Completion")
    
    # Filter for Coordinator's Dept
    my_events = [e for e in st.session_state['events'] if e['dept'] == user_dept]
    
    if my_events:
        df_my = pd.DataFrame(my_events)
        # Formatting for display
        df_display = df_my[['id', 'name', 'venue', 'start_time', 'end_time', 'status']].copy()
        st.dataframe(df_display, use_container_width=True)

        # Event Completion Action
        st.write("### Actions")
        # List events that are 'Final Approved' and can be ended, or 'Pending'
        active_events = [e for e in my_events if e['status'] == 'Final Approved']
        if active_events:
            evt_to_end = st.selectbox("Select Event to Mark Completed", active_events, format_func=lambda x: f"{x['name']} ({x['id']})")
            if st.button("End Event & Release Resources"):
                # Find and update
                for e in st.session_state['events']:
                    if e['id'] == evt_to_end['id']:
                        e['status'] = 'Completed'
                        st.success(f"Event '{e['name']}' marked as Completed. Resources released.")
                        st.rerun()
        else:
            st.info("No active events to complete.")
            
# --- VIEW: HOD (Head of Department) ---------------------------------------------
elif role == "HOD":
    st.header(f"📋 HOD Approval Dashboard ({user_dept})")
    
    # Needs: Pending approvals for THEIR dept
    pending_approvals = [e for e in st.session_state['events'] if e['dept'] == user_dept and e['status'] == 'Pending']
    
    if not pending_approvals:
        st.info("No pending approvals for your department.")
    else:
        for event in pending_approvals:
            with st.expander(f"{event['name']} | {event['venue']} | {event['start_time'].strftime('%Y-%m-%d %H:%M')}"):
                st.write(f"**Coordinator:** {event['coordinator']}")
                st.write(f"**Equipment:** {', '.join(event['equipment'])}")
                
                col1, col2 = st.columns(2)
                if col1.button("Approve", key=f"hod_app_{event['id']}"):
                    event['status'] = "HOD Approved"
                    st.success("Approved!")
                    st.rerun()
                if col2.button("Reject", key=f"hod_rej_{event['id']}"):
                    event['status'] = "Rejected"
                    st.error("Rejected.")
                    st.rerun()

# --- VIEW: Dean -----------------------------------------------------------------
elif role == "Dean":
    st.header("🎓 Dean Approval Dashboard")
    
    # Needs: HOD Approved events (All Depts)
    dean_approvals = [e for e in st.session_state['events'] if e['status'] == 'HOD Approved']
    
    if not dean_approvals:
        st.info("No events awaiting Dean approval.")
    else:
        for event in dean_approvals:
            with st.expander(f"{event['dept']}: {event['name']} | {event['venue']}"):
                st.write(f"**Time:** {event['start_time']} - {event['end_time']}")
                
                col1, col2 = st.columns(2)
                if col1.button("Approve", key=f"dean_app_{event['id']}"):
                    event['status'] = "Dean Approved"
                    st.success("Approved!")
                    st.rerun()
                if col2.button("Reject", key=f"dean_rej_{event['id']}"):
                    event['status'] = "Rejected"
                    st.error("Rejected.")
                    st.rerun()

# --- VIEW: Institutional Head ---------------------------------------------------
elif role == "Institutional Head":
    st.header("🏫 Final Approval Dashboard")
    
    # Needs: Dean Approved events
    head_approvals = [e for e in st.session_state['events'] if e['status'] == 'Dean Approved']
    
    if not head_approvals:
        st.info("No events awaiting Final approval.")
    else:
        for event in head_approvals:
            with st.expander(f"{event['dept']}: {event['name']} | {event['venue']}"):
                st.write(f"**Time:** {event['start_time']} - {event['end_time']}")
                
                col1, col2 = st.columns(2)
                if col1.button("Final Approve", key=f"head_app_{event['id']}"):
                    event['status'] = "Final Approved"
                    st.success("Event has been Finally Approved!")
                    st.rerun()
                if col2.button("Reject", key=f"head_rej_{event['id']}"):
                    event['status'] = "Rejected"
                    st.error("Rejected.")
                    st.rerun()

# --- VIEW: Admin ----------------------------------------------------------------
elif role == "Admin":
    st.header("🛠️ Admin Resource Management")
    
    st.subheader("Venue Capacities")
    
    # Simple form to update capacities
    venues = st.session_state['venues']
    for v_name, v_cap in venues.items():
        new_cap = st.number_input(f"Capacity: {v_name}", value=v_cap, key=f"cap_{v_name}")
        if new_cap != v_cap:
            st.session_state['venues'][v_name] = new_cap
            st.toast(f"Updated capacity for {v_name}")

    st.subheader("Global Event Log (Audit)")
    all_events = st.session_state['events']
    if all_events:
        st.dataframe(pd.DataFrame(all_events).drop(columns=['start_time', 'end_time']).assign(
            Start=[e['start_time'].strftime('%Y-%m-%d %H:%M') for e in all_events],
            End=[e['end_time'].strftime('%Y-%m-%d %H:%M') for e in all_events]
        ))

# --------------------------------------------------------------------------------
# 5. Visualization (Global Occupancy View - Visible to Admin & Heads)
# --------------------------------------------------------------------------------
# Coordinators cannot see this global view per requirements "Coordinators cannot see the 'Global Occupancy' view"
if role not in ["Event Coordinator"]:
    st.markdown("---")
    st.header("📊 Global Resource Occupancy")
    
    # Prepare data for plotting
    active_events = [e for e in st.session_state['events'] if e['status'] not in ['Rejected', 'Completed']]
    
    if active_events:
        df = pd.DataFrame(active_events)
        
        # Gantt Chart using Plotly
        fig = px.timeline(
            df, 
            x_start="start_time", 
            x_end="end_time", 
            y="venue", 
            color="dept", 
            hover_data=["name", "status"],
            title="Venue Usage Timeline"
        )
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No active events to display in timeline.")
