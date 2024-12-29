import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns
from plotfunctions.linechart import LineChartClass
from plotfunctions.targetchart import TargetChartClass
from utils.create_user_df import inputdf_to_userdf  

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Main app styling */
    body {
      background: linear-gradient(to right, #eef2f3, #8e9eab);
      font-family: 'Arial', san-serif;
      color: #2c3e50;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
      background: linear-gradient(120deg, #1e3c72, #2a5298);
      color: white;
    }
    .sidebar-content {
      font-size: 18px;
      font-weight: bold;
    }

    /* Table styling */
    .dataframe {
      border-collapse: collapse;
      width: 100%;
    }
    .dataframe th, .dataframe td {
      border: 1px solid #ddd;
      padding: 8px;
    }
    .dataframe tr:nth-child(even) {
      background-color: #f2f2f2;
    }
    .dataframe th {
      padding-top: 12px;
      padding-bottom: 12px;
      text-align: left;
      background-color: #4CAF50;
      color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for rows
if "patients_data_list" not in st.session_state:
    st.session_state["patients_data_list"] = [{"months": "Jan", "ICU": 0, "Post-ICU": 0, "Twin-Share-Cabin": 0,
                                               "Single-Cabin": 0, "General-Male-Ward": 0, "General-Female-Ward": 0}]

room_types = ["ICU", "Post-ICU", "Twin-Share-Cabin", "Single-Cabin", "General-Male-Ward", "General-Female-Ward"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Function to display rows in the sidebar
def display_rows():
    indices_to_delete = []
    for idx, row in enumerate(st.session_state["patients_data_list"]):
        st.sidebar.markdown(f"### DATA NO: {idx + 1}")
        row["months"] = st.sidebar.selectbox(f"Enter Month", months, index=months.index(row["months"]),
                                             key=f"month_{idx}")
        for unit in room_types:
            row[unit] = st.sidebar.number_input(f"Patients in {unit}", min_value=0, max_value=1000,
                                                value=row[unit], key=f"{unit}_{idx}")
        # Delete button for each row
        if st.sidebar.button(f"Delete Data {idx + 1}", key=f"delete_{idx}"):
            indices_to_delete.append(idx)

    # Delete rows after loop to avoid modifying list while iterating
    if indices_to_delete:
        for idx in sorted(indices_to_delete, reverse=True):
            del st.session_state["patients_data_list"][idx]

# Add a new row
def add_row():
    st.session_state["patients_data_list"].append(
        {"months": "Jan", "ICU": 0, "Post-ICU": 0, "Twin-Share-Cabin": 0,
         "Single-Cabin": 0, "General-Male-Ward": 0, "General-Female-Ward": 0}
    )

st.sidebar.header("Add Number of Patients in Each Unit")
display_rows()

if st.sidebar.button("Add More Rows"):
    add_row()

# ______________________________________________Main app___________________________________________________________

st.markdown("<h1><span style='color: blue;'>DIPLOMAT NURSING HOME</span></h1>", unsafe_allow_html=True)
st.markdown("### Predictive Analysis of Monthly Income and Target")
st.markdown("#### Number of Patients in Each Unit")

input_df = pd.DataFrame(st.session_state["patients_data_list"])
st.dataframe(input_df.style.set_properties(
    **{'background-color': '#f9f9f9', 'color': '#2c3e50', 'border-color': '#ccc'}
).set_table_styles(
    [{'selector': 'th', 'props': [('background-color', '#3498db'), ('color', 'white'), ('text-align', 'center')]}]
))


user_df = inputdf_to_userdf(input_df, r"csv\user_input.csv", r"model\sample_model.joblib")
if user_df.shape[0] > 0:
    
    
    plot_linechart = LineChartClass(r"csv\user_input.csv", r"model\sample_model.joblib", user_df)

  
    plot_targetchart = TargetChartClass(r"csv\user_input.csv", r"model\sample_model.joblib", user_df)
    plot_linechart.predictive_line_chart()
    plot_targetchart.monthly_target_maxline_and_thresholdline()
else:
    st.warning("No data available for predictive analysis!")
