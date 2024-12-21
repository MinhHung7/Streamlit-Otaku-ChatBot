import streamlit as st
import pandas as pd
import papermill as pm
import os

# Set the page title
st.set_page_config(page_title="Data Upload and Preprocessing", page_icon="📥")

# Title of the page
st.title("Upload Your Anime Dataset")

# Instructions for the user
st.markdown("""
Please upload a CSV file containing anime data. The dataset will be processed and visualized in later steps. 

The file should contain relevant columns, such as anime title, genre, rating, and production studio.

### Allowed File Format:
- Only CSV files are allowed. 
""")

# Function to clear cache before running
def clear_cache():
    # For Streamlit versions 1.14 and later
    try:
        st.cache_resource.clear()
    except AttributeError:
        pass  # st.cache_data may not be available in older versions

# Call cache clearing function before uploading the file or processing
clear_cache()

# File uploader widget to upload a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

# Check if a file is uploaded
if uploaded_file is not None:
    st.write(f"Uploaded file: {uploaded_file.name}")

    # Ensure the directory exists before saving the file
    # save_dir = "./raw_animes_dataset/"
    # if not os.path.exists(save_dir):
    #     os.makedirs(save_dir)  # Create the directory if it doesn't exist

    # Save the uploaded file temporarily
    # save_path = os.path.join(save_dir, uploaded_fi
    # le.name)

    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read the CSV file into a pandas dataframe
    df = pd.read_csv(uploaded_file)
    
    # Display the uploaded dataset's basic information
    st.subheader("Dataset Information")
    
    # Show the first few rows of the dataset
    st.write("Preview of the dataset:")
    st.write(df.head())
    
    # Show the basic details of the dataset (shape, columns, etc.)
    st.write(f"Number of rows: {df.shape[0]}")
    st.write(f"Number of columns: {df.shape[1]}")
    st.write("Columns in the dataset:")
    st.write(df.columns.tolist())
    
    if st.button("Data Preprocessing"):
        st.write("Please wait.")

        # Specify the notebook path
        data_preprocessing_notebook_path = "anime_data_processing.ipynb"
        
        # Output path for the executed notebook
        output_notebook_path = "processed_output.ipynb"

        try:
            # Run the notebook using papermill
            pm.execute_notebook(
                data_preprocessing_notebook_path,          # Input notebook path
                output_notebook_path,   # Output notebook path
            )
            st.success("Notebook executed successfully!")
            st.write("Processed notebook saved as `processed_output.ipynb`. You can check it here.")

        # Option to download the processed output notebook
            with open(output_notebook_path, "rb") as f:
                st.download_button(
                    label="Download Processed Notebook",
                    data=f,
                    file_name="processed_output.ipynb",
                    mime="application/octet-stream"
                )
            
            df = pd.read_csv(r"anime-data-preprocessing.csv")
            st.session_state.csv_file = df.to_csv(index=False)
            
            # Option to download the dataset after preprocessing (if needed)
            st.download_button(
                label="Download preprocessing dataset",
                data=st.session_state.csv_file,
                file_name="anime-data-preprocessing.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Error running the notebook: {str(e)}")

else:
    st.write("No file uploaded yet. Please upload a CSV file to begin.")

