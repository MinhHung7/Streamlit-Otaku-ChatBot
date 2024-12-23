import streamlit as st
import pandas as pd
import io
from streamlist_pandas import filter_string, create_widgets, filter_df
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import datetime as dt
from ydata_profiling import ProfileReport

# Set the page title
st.set_page_config(page_title="Report Generator", page_icon="🗒️")

# Title of the page
st.title("Report Generator")

if 'csv_file' in st.session_state:

    # Read the CSV from session state into DataFrame
    df = pd.read_csv(io.StringIO(st.session_state.csv_file))
    
    st.write("Overview of dataframe")

    # Display the DataFrame
    st.write(df)

    ###########################################
    st.sidebar.title("Control Panel")

    create_data = {}  # define this as needed, e.g. {'column_name': 'multiselect'}
    ignore_columns = []  # You can ignore specific columns if necessary
    all_widgets = create_widgets(df, create_data=create_data, ignore_columns=ignore_columns)

    # Step 4: Apply filtering based on user input from sidebar
    filtered_df = filter_df(df, all_widgets)
    
    if st.button("Report Generating"):

        profile = ProfileReport(filtered_df)  # or provide a valid path
        profile.to_file("report.html")

        # Read and display the HTML file in Streamlit
        with open("report.html", "r") as f:
            html_content = f.read()

        # Display the HTML content in Streamlit
        st.components.v1.html(html_content, height=1000, scrolling=True)

    ###########################################################
else:
    st.write("Please create and download a CSV first!")


