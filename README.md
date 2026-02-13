# ResourceFlow - The Institutional Event Governance Platform 🏛️

**ResourceFlow** is a streamlined, single-file institutional event management system built with Python and Streamlit. It demonstrates "Conflict-Aware Governance" for handling venue bookings, approvals, and resource management in an academic setting.

![Status](https://img.shields.io/badge/Status-Prototype-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-FF4B4B)

## 🌟 Key Features

*   **Role-Based Access Control (RBAC)**: Distinct interfaces for Event Coordinators, HODs, Deans, Institutional Heads, and Admins.
*   **Conflict Detection Engine**: Real-time checking of venue availability to prevent booking clashes.
*   **Multi-Level Approval Workflow**:
    *   `Pending` → `HOD Approved` → `Dean Approved` → `Final Approved`
*   **Resource Management**: Admin controls for venue capacities and global logging.
*   **Premium UI**: Custom "Deep Space" glassmorphism design for a modern look.
*   **Interactive Visualization**: Gantt charts for tracking global resource occupancy.

## 🚀 Getting Started

### Prerequisites

*   Python 3.8 or higher
*   pip (Python package manager)

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/resourceflow.git
    cd resourceflow
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Run the application using Streamlit:

```bash
streamlit run app.py
```

*Note: If `streamlit` is not in your PATH, use `python -m streamlit run app.py`*

## 📖 Usage Guide

Use the **Sidebar** to switch between roles and test the governance flow:

1.  **Event Coordinator**: 
    *   Select your Department.
    *   Fill out the "New Event Request" form.
    *   **Try causing a conflict**: Book "Main Auditorium" for a time that overlaps with an existing event.
2.  **HOD (Head of Department)**:
    *   Login to approve events requested by your department.
3.  **Dean / Institutional Head**:
    *   Review and grant higher-level approvals.
4.  **Admin**:
    *   Adjust venue capacities and view the global audit log.

## 🛠️ Built With

*   [Streamlit](https://streamlit.io/) - The fastest way to build data apps in Python.
*   [Pandas](https://pandas.pydata.org/) - Data manipulation and analysis.
*   [Plotly](https://plotly.com/) - Interactive graphing library.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
