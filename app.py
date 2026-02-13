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
import requests
from streamlit_lottie import st_lottie

# --------------------------------------------------------------------------------
# 0. UI Configuration & Ultra-Premium Custom CSS
# --------------------------------------------------------------------------------
st.set_page_config(page_title="ResourceFlow", layout="wide", page_icon="🏛️", initial_sidebar_state="expanded")

# Custom CSS for Premium Look
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
            background: rgba(10, 8, 30, 0.95);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 10px 0 30px rgba(0,0,0,0.5);
        }
        
        /* Fade In Animation for Content */
        .element-container {
            animation: fadeIn 0.8s ease-in-out;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
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
        
        /* Metric Cards */
        div[data-testid="stMetric"] {
            background-color: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
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
# Helper: Load Lottie Animation
# --------------------------------------------------------------------------------
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_event = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_jcikwtux.json")
lottie_login = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_mjlh3hcy.json")

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
        st.session_state['departments'] = ['CSE', 'ECE', 'MECH', 'CIVIL']

        # Dummy Equipment
        st.session_state['equipment'] = ['Projector', 'Sound System', 'Whiteboard', 'Webcam', 'Podium']
        
        # Dummy Events
        # Status Workflow: Pending -> HOD Approved -> Dean Approved -> Final Approved
        st.session_state['events'] = [
            {
                'id': 1,
                'name': 'AI Workshop',
                'dept': 'CSE',
                'coordinator': 'Prof. Alan',
                'venue': 'Conference Room A',
                'start_time': datetime.datetime.now() + datetime.timedelta(days=1, hours=2),
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
            }
        ]
        st.session_state['initialized'] = True
    
    # Login State
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user_role'] = None
        st.session_state['user_dept'] = None
        st.session_state['user_name'] = None

init_data()

# --------------------------------------------------------------------------------
# 2. Authentication System
# --------------------------------------------------------------------------------
USERS = {
    "admin": {"password": "123", "role": "Admin", "dept": "ALL", "name": "System Admin"},
    "cse_coord": {"password": "123", "role": "Event Coordinator", "dept": "CSE", "name": "Prof. Alan"},
    "ece_coord": {"password": "123", "role": "Event Coordinator", "dept": "ECE", "name": "Dr. Circuit"},
    "hod_cse": {"password": "123", "role": "HOD", "dept": "CSE", "name": "Dr. Turing"},
    "dean": {"password": "123", "role": "Dean", "dept": "ALL", "name": "Dean Smith"},
    "head": {"password": "123", "role": "Institutional Head", "dept": "ALL", "name": "Dr. Director"}
}

def login_page():
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🚀 Welcome to ResourceFlow</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if lottie_login:
            st_lottie(lottie_login, height=400, key="login_anim")
        else:
            st.image("https://cdn-icons-png.flaticon.com/512/3209/3209990.png", width=300)
            
    with col2:
        st.markdown("""
            <div style='background: rgba(255,255,255,0.05); padding: 40px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);'>
                <h2 style='text-align: center; color: #fff;'>Login</h2>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Access Dashboard", use_container_width=True)
            
            if submitted:
                if username in USERS and USERS[username]['password'] == password:
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = USERS[username]['role']
                    st.session_state['user_dept'] = USERS[username]['dept']
                    st.session_state['user_name'] = USERS[username]['name']
                    st.balloons()
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
        
        st.caption("💡 **Demo Credentials** (Pass: 123): `admin`, `cse_coord`, `hod_cse`, `dean`, `head`")

def logout():
    st.session_state['logged_in'] = False
    st.session_state['user_role'] = None
    st.session_state['user_dept'] = None
    st.rerun()

# --------------------------------------------------------------------------------
# 3. Conflict Detection Engine (CRITICAL)
# --------------------------------------------------------------------------------
def check_availability(start_time, end_time, venue, current_event_id=None):
    """
    Checks if the venue is available for the given time slot.
    Returns: (is_available: bool, message: str)
    """
    for event in st.session_state['events']:
        if current_event_id and event['id'] == current_event_id:
            continue
        if event['status'] in ['Rejected', 'Completed']:
            continue

        if event['venue'] == venue:
            if start_time < event['end_time'] and end_time > event['start_time']:
                return False, f"Conflict: {venue} is booked by Dept {event['dept']} for '{event['name']}' from {event['start_time'].strftime('%H:%M')} to {event['end_time'].strftime('%H:%M')}."
    return True, "Available"

# --------------------------------------------------------------------------------
# 4. Main Application Logic
# --------------------------------------------------------------------------------

# --- Persistent Sidebar (Always Visible) ---
with st.sidebar:
    # App Logo/Header
    st.image("https://cdn-icons-png.flaticon.com/512/3209/3209990.png", width=60)
    st.markdown("<h2 style='display: inline-block; vertical-align: middle; margin-left: 10px;'>ResourceFlow</h2>", unsafe_allow_html=True)
    st.markdown("---")

if not st.session_state['logged_in']:
    # Sidebar Content for Guest/Login Mode
    with st.sidebar:
        st.info("🔐 **Secure Access Required**\n\nPlease log in to manage institutional resources and approvals.")
        st.markdown("### System Status\n🟢 **Online**\n\nv1.2.0-stable")
    
    login_page()
else:
    # --- Sidebar Content for Logged In Users ---
    role = st.session_state['user_role']
    user_dept = st.session_state['user_dept']
    user_name = st.session_state['user_name']
    
    with st.sidebar:
        # User Profile Section
        if lottie_event:
            st_lottie(lottie_event, height=100, key="menu_anim")
        
        st.divider()
        st.markdown(f"""
        <div style="background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="margin:0; color:white;">{user_name}</h3>
            <p style="margin:0; font-size: 0.9em; color: #bbb;">{role}</p>
            <p style="margin:0; font-size: 0.8em; color: #e52e71;">{user_dept} Department</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation (Future Proofing)
        st.markdown("### 🧭 Navigation")
        nav_mode = st.radio("Go to:", ["Dashboard", "All Events", "Settings"], label_visibility="collapsed")
        
        st.divider()
        
        # Logout Section
        st.markdown("### ⚙️ Account")
        if st.button("🚪 Sign Out", key="sidebar_logout_btn", use_container_width=True):
            with st.spinner("Logging out..."):
                logout()
        
        st.caption("ResourceFlow v2.0 • Online")

    # --- Live Stats Row ---
    st.title(f"{nav_mode if nav_mode != 'Dashboard' else 'ResourceFlow Dashboard'}")
    
    # Calculate Stats
    total_events = len(st.session_state['events'])
    pending_count = len([e for e in st.session_state['events'] if e['status'] == 'Pending'])
    my_dept_events = len([e for e in st.session_state['events'] if e['dept'] == user_dept]) if user_dept != "ALL" else total_events
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Events", total_events, "+1 today")
    m2.metric("Pending Approvals", pending_count, "Urgent", delta_color="inverse")
    m3.metric("Dept Activity", my_dept_events, "Active")
    m4.metric("System Status", "Online", "🟢")
    
    st.markdown("---")

    # --- VIEW: Event Coordinator ------------------------------------------------
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
                evt_desc = st.text_area("Event Description / Purpose")

            submit = st.form_submit_button("Check Availability & Submit")

        if submit:
            start_dt = datetime.datetime.combine(d, t_start)
            end_dt = datetime.datetime.combine(d, t_end)

            if end_dt <= start_dt:
                st.error("End time must be after start time.")
            else:
                is_avail, msg = check_availability(start_dt, end_dt, evt_venue)
                if not is_avail:
                    st.error(f"❌ {msg}")
                else:
                    new_id = max([e['id'] for e in st.session_state['events']]) + 1 if st.session_state['events'] else 1
                    new_event = {
                        'id': new_id,
                        'name': evt_name,
                        'dept': user_dept,
                        'coordinator': user_name,
                        'venue': evt_venue,
                        'start_time': start_dt,
                        'end_time': end_dt,
                        'equipment': evt_equip,
                        'description': evt_desc,
                        'status': 'Pending',
                        'feedback': ''
                    }
                    st.session_state['events'].append(new_event)
                    st.success(f"✅ Event '{evt_name}' requested successfully! Status: Pending")

        st.subheader("My Department Events")
        my_events = [e for e in st.session_state['events'] if e['dept'] == user_dept]
        if my_events:
            df_my = pd.DataFrame(my_events)
            st.dataframe(df_my[['id', 'name', 'venue', 'start_time', 'end_time', 'status', 'feedback']], use_container_width=True)
            
            # Action: Cancel Pending Event
            pending_my = [e for e in my_events if e['status'] == 'Pending']
            if pending_my:
                evt_to_cancel = st.selectbox("Cancel Pending Request", pending_my, format_func=lambda x: f"{x['name']} ({x['id']})")
                if st.button("Cancel Request"):
                    st.session_state['events'].remove(evt_to_cancel)
                    st.success("Request Cancelled.")
                    st.rerun()
            
            # Completion
            active_events = [e for e in my_events if e['status'] == 'Final Approved']
            if active_events:
                evt_to_end = st.selectbox("Select Event to Mark Completed", active_events, format_func=lambda x: f"{x['name']} ({x['id']})")
                if st.button("End Event & Release Resources"):
                    for e in st.session_state['events']:
                        if e['id'] == evt_to_end['id']:
                            e['status'] = 'Completed'
                            st.success(f"Event '{e['name']}' marked as Completed.")
                            st.rerun()

    # --- VIEW: HOD --------------------------------------------------------------
    elif role == "HOD":
        st.header(f"📋 HOD Approval Dashboard ({user_dept})")
        pending_approvals = [e for e in st.session_state['events'] if e['dept'] == user_dept and e['status'] == 'Pending']
        
        if not pending_approvals:
            st.info("No pending approvals.")
        else:
            for event in pending_approvals:
                with st.expander(f"{event['name']} | {event['venue']} | {event['start_time']}"):
                    st.write(f"**Coordinator:** {event['coordinator']}")
                    st.write(f"**Description:** {event.get('description', 'N/A')}")
                    st.write(f"**Equipment:** {', '.join(event['equipment'])}")
                    
                    feedback = st.text_input("Feedback/Reason (Optional)", key=f"feed_{event['id']}")
                    
                    col1, col2 = st.columns(2)
                    if col1.button("Approve", key=f"hod_app_{event['id']}"):
                        event['status'] = "HOD Approved"
                        event['feedback'] = feedback
                        st.balloons()
                        st.rerun()
                    if col2.button("Reject", key=f"hod_rej_{event['id']}"):
                        event['status'] = "Rejected"
                        event['feedback'] = feedback
                        st.error("Rejected.")
                        st.rerun()

    # --- VIEW: Dean -------------------------------------------------------------
    elif role == "Dean":
        st.header("🎓 Dean Approval Dashboard")
        
        # Analytics for Dean (Enhanced)
        st.subheader("📊 Department Analytics")
        if st.session_state['events']:
            df_analytics = pd.DataFrame(st.session_state['events'])
            
            # 1. Events per Department (Bar Chart)
            dept_counts = df_analytics['dept'].value_counts().reset_index()
            dept_counts.columns = ['Department', 'Count']
            
            fig_dept = px.bar(
                dept_counts, 
                x='Department', 
                y='Count', 
                color='Department', 
                title='Events by Department',
                text='Count',
                template='plotly_dark'
            )
            st.plotly_chart(fig_dept, use_container_width=True)
        
        dean_approvals = [e for e in st.session_state['events'] if e['status'] == 'HOD Approved']
        
        st.subheader("Pending Approvals")
        if not dean_approvals:
            st.info("No pending approvals.")
        else:
            for event in dean_approvals:
                with st.expander(f"{event['dept']}: {event['name']} | {event['venue']}"):
                    st.write(f"**Desc:** {event.get('description', 'N/A')}")
                    st.write(f"**HOD Feedback:** {event.get('feedback', 'None')}")
                    
                    feedback = st.text_input("Dean's Note", key=f"dean_note_{event['id']}")
                    
                    col1, col2 = st.columns(2)
                    if col1.button("Approve", key=f"dean_app_{event['id']}"):
                        event['status'] = "Dean Approved"
                        event['feedback'] += f" | Dean: {feedback}"
                        st.success("Approved!")
                        st.rerun()
                    if col2.button("Reject", key=f"dean_rej_{event['id']}"):
                        event['status'] = "Rejected"
                        event['feedback'] += f" | Dean: {feedback}"
                        st.error("Rejected.")
                        st.rerun()

    # --- VIEW: Institutional Head -----------------------------------------------
    elif role == "Institutional Head":
        st.header("🏫 Final Approval Dashboard")
        
        # Head Analytics
        if st.session_state['events']:
            st.subheader("📈 Institutional Overview")
            df_head = pd.DataFrame(st.session_state['events'])
            
            c1, c2 = st.columns(2)
            with c1:
                # Status Distribution Pie Chart
                status_counts = df_head['status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                fig_status = px.pie(
                    status_counts, 
                    values='Count', 
                    names='Status', 
                    title='Overall Event Status',
                    hole=0.4,
                    template='plotly_dark'
                )
                st.plotly_chart(fig_status, use_container_width=True)
            
            with c2:
                 # Venue Utilization
                venue_counts = df_head['venue'].value_counts().reset_index()
                venue_counts.columns = ['Venue', 'Usage Count']
                fig_venue = px.bar(
                    venue_counts, 
                    x='Venue', 
                    y='Usage Count', 
                    color='Venue', 
                    title='Venue Utilization',
                    template='plotly_dark'
                )
                st.plotly_chart(fig_venue, use_container_width=True)

        head_approvals = [e for e in st.session_state['events'] if e['status'] == 'Dean Approved']
        
        if not head_approvals:
            st.info("No pending approvals.")
        else:
            for event in head_approvals:
                with st.expander(f"{event['dept']}: {event['name']}"):
                    st.info(f"Prior Approvals: {event.get('feedback', 'None')}")
                    col1, col2 = st.columns(2)
                    if col1.button("Final Approve", key=f"head_app_{event['id']}"):
                        event['status'] = "Final Approved"
                        st.success("Event has been Finally Approved!")
                        st.balloons()
                        st.rerun()
                    if col2.button("Reject", key=f"head_rej_{event['id']}"):
                        event['status'] = "Rejected"
                        st.error("Rejected.")
                        st.rerun()

    # --- VIEW: Admin (ENHANCED) -------------------------------------------------
    elif role == "Admin":
        st.header("🛠️ Admin Master Control")
        
        tabs = st.tabs(["🏛️ Venues & Equipment", "📝 Event Manager", "📊 Global Logs", "📈 Analytics"])
        
        # Tab 1: Resource Management
        with tabs[0]:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Manage Venues")
                # Add Venue
                with st.expander("➕ Add New Venue"):
                    new_venue_name = st.text_input("Venue Name")
                    new_venue_cap = st.number_input("Capacity", min_value=10, value=50)
                    if st.button("Add Venue"):
                        if new_venue_name and new_venue_name not in st.session_state['venues']:
                            st.session_state['venues'][new_venue_name] = new_venue_cap
                            st.success(f"Added {new_venue_name}")
                            st.rerun()
                        else:
                            st.warning("Invalid name or already exists.")
                
                # Edit Capacities
                for v_name, v_cap in st.session_state['venues'].items():
                    c1, c2 = st.columns([3, 1])
                    c1.write(f"**{v_name}**")
                    new_cap = c2.number_input("Cap", value=v_cap, key=f"edit_cap_{v_name}", label_visibility="collapsed")
                    if new_cap != v_cap:
                        st.session_state['venues'][v_name] = new_cap
                        st.toast(f"Updated {v_name} capacity")

            with col2:
                st.subheader("Manage Equipment")
                # Add Equipment
                with st.form("add_equip_form"):
                    new_equip = st.text_input("Equipment Name")
                    if st.form_submit_button("Add Equipment"):
                        if new_equip and new_equip not in st.session_state['equipment']:
                            st.session_state['equipment'].append(new_equip)
                            st.success(f"Added {new_equip}")
                            st.rerun()
                
                # List Equipment
                st.write("Current Inventory:")
                for equip in st.session_state['equipment']:
                    st.code(equip)

        # Tab 2: Event Editor (Super Admin Power)
        with tabs[1]:
            st.subheader("✏️ Edit Any Event")
            all_events = st.session_state['events']
            if all_events:
                event_to_edit = st.selectbox("Select Event to Edit", all_events, format_func=lambda x: f"{x['id']}: {x['name']} ({x['status']})")
                
                with st.form("admin_edit_event"):
                    e_name = st.text_input("Name", event_to_edit['name'])
                    e_venue = st.selectbox("Venue", list(st.session_state['venues'].keys()), index=list(st.session_state['venues'].keys()).index(event_to_edit['venue']) if event_to_edit['venue'] in st.session_state['venues'] else 0)
                    e_status = st.selectbox("Status", ["Pending", "HOD Approved", "Dean Approved", "Final Approved", "Completed", "Rejected"], index=["Pending", "HOD Approved", "Dean Approved", "Final Approved", "Completed", "Rejected"].index(event_to_edit['status']))
                    
                    if st.form_submit_button("Update Event"):
                        # In a real app, you'd check conflicts here too, but Admin has override power
                        event_to_edit['name'] = e_name
                        event_to_edit['venue'] = e_venue
                        event_to_edit['status'] = e_status
                        st.success("Event Updated Successfully!")
                        st.rerun()
            else:
                st.info("No events to edit.")

        # Tab 3: Global Logs
        with tabs[2]:
            st.dataframe(pd.DataFrame(st.session_state['events']))

        # Tab 4: Admin Analytics (New)
        with tabs[3]:
            st.subheader("Deep Dive Analytics")
            if st.session_state['events']:
                df_admin = pd.DataFrame(st.session_state['events'])
                
                # 3D Scatter Plot (Time vs Venue)
                fig_3d = px.scatter_3d(
                    df_admin,
                    x='dept',
                    y='venue',
                    z='id',
                    color='status',
                    size_max=18,
                    opacity=0.7,
                    title="3D Event Distribution",
                    template='plotly_dark'
                )
                st.plotly_chart(fig_3d, use_container_width=True)
                
                # Heatmap of Activity by Hour (Simulation)
                st.write("**Busy Hours Heatmap (Simulated)**")
                # Create dummy hour data for visualization
                df_admin['hour'] = df_admin['start_time'].dt.hour
                fig_heat = px.density_heatmap(
                    df_admin, 
                    x='start_time', 
                    y='venue', 
                    z='id', 
                    title="Venue Traffic Heatmap",
                    template='plotly_dark'
                )
                st.plotly_chart(fig_heat, use_container_width=True)

    # --------------------------------------------------------------------------------
    # 5. Visualization (Global Occupancy View - Visible to Admin & Heads)
    # --------------------------------------------------------------------------------
    if role in ["Admin", "Institutional Head", "Dean"]:
        st.markdown("---")
        st.header("📊 Global Resource Occupancy")
        
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
                title="Venue Usage Timeline",
                template="plotly_dark"
            )
            fig.update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No active events to display in timeline.")
