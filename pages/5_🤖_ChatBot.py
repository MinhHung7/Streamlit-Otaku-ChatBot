import streamlit as st
import pandas as pd
import io
from io import StringIO
import os
import matplotlib
import matplotlib.pyplot as plt
from translate import Translator
from pandasai import SmartDataframe
from pandasai.responses.streamlit_response import StreamlitResponse
from pandasai.engine import set_pd_engine

set_pd_engine("pandas")

# Streamlit app layout
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
st.title("💬 Chatbot")

export_folder = os.path.join(os.getcwd(), "exports/charts")

if 'csv_file' in st.session_state:

    # Read the CSV from session state into DataFrame
    df = pd.read_csv(io.StringIO(st.session_state.csv_file))

    translator = Translator(to_lang="en", from_lang="vi")

    os.environ["PANDASAI_API_KEY"] = "$2a$10$GEsfXrwFuOWndHnBgXcSkecd3RlY3ffzDyDk19gXMRue4Dr.oqz4m"

    sdf = SmartDataframe(df, config={"save_charts": True,"save_charts_path": export_folder, "verbose": True, "response_parser": StreamlitResponse, "custom_whitelisted_dependencies": ["to_numeric"]})

    # User input
    user_input = st.text_area("You: ", "")
    # Create a submit button
    submit_button = st.button("Submit")

    if submit_button and user_input:

        for filename in os.listdir(export_folder):
            file_path = os.path.join(export_folder, filename)
            # Check if it's a file (not a folder)
            if os.path.isfile(file_path):
                os.remove(file_path)

        translated_text = translator.translate(user_input)

        response = sdf.chat(translated_text)

        for filename in os.listdir(export_folder):
            file_path = os.path.join(export_folder, filename)
            # Check if it's a file (not a folder)
            if os.path.isfile(file_path):
                st.image(file_path)

        if isinstance(response, pd.DataFrame):
            # Display the DataFrame directly
            st.write(f"🤖 Chatbot:")
            st.write(response)
        else:
            # If the response is a string (e.g., some text or CSV), handle it accordingly
            # For example, if it's a CSV-like string:
            st.write(f"🤖 Chatbot: {response}")

else:
    st.write("Please create and download a CSV first!")