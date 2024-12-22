import streamlit as st

st.set_page_config(
    page_title="Anime Analysics App",
    page_icon="🏠",
)

st.title("Anime 2023 Analysis & Machine Learning Hub")
st.markdown("""### Hello there 🖐
This is my first project about buidling an analysis app using [Streamlit](https://streamlit.io/)

In order to test successfully, you need to use [anime-dataset-2023.csv](https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset?select=anime-dataset-2023.csv), which my team analyse in final project in **Data Science Programming**
            
---
If you're curious about our final project, you can visit here [Final Project Data Science Programming](https://github.com/MinhHung7/Final_Project_DataScienceProgramming)

### 👉 Here are some information about this app
""")

with st.expander("Introduction"):
    st.markdown("""Welcome to the Anime 2023 Analysis & Machine Learning Hub, a comprehensive exploration of anime data through the power of data science and machine learning. This app is an integration of techniques learned in `Data Science Programming, Data Visualization, and Data Science Introduction` courses, where we analyze and model the Anime Dataset 2023.""")
    st.markdown("""Our journey begins with data preprocessing, where we clean, organize, and prepare the dataset to ensure it is ready for meaningful analysis. Following that, we delve into data visualization, using various graphical techniques to uncover hidden trends, relationships, and patterns within the dataset, such as correlations between anime genres, ratings, and production factors.""") 
    st.markdown("""Finally, we apply machine learning models to predict outcomes such as age ratings, recommend anime based on user preferences, and optimize production strategies. This app not only demonstrates the power of data science but also provides practical insights that can transform how we understand and interact with the anime industry.""")

with st.expander("Keys Features and Objectives"):
    st.markdown("""
    🛠️ **Upload and preprocess datasets**: Seamlessly upload and prepare your anime dataset for analysis.
    
    📊 **Explore data with visualizations**: Use interactive visualizations to discover patterns and trends in the anime industry.
    
    🤖 **Build and evaluate machine learning models**: Create predictive models to classify, recommend, and optimize anime-related data.
    
    📥 **Generate insights and downloadable reports**: Get actionable insights and download detailed reports to support decision-making.
    """)

# Simple Instructions
with st.expander("Navigation Instructions"):
    st.markdown("""
    - 🧭 **Use the sidebar**: The sidebar allows you to easily move between key pages such as:
        - **Data Upload**: Upload your anime dataset to get started.
        - **Exploratory Data Analysis (EDA)**: Visualize and analyze the data to uncover insights.
        - **Model Training**: Build and evaluate machine learning models.
        - **Reports**: Download insights and detailed reports generated from your analysis.
    """)
    # Optionally, you can guide users further on how to use the sidebar for navigation
    st.markdown("""
    For more detailed navigation, look at the **sidebar** on the left of the screen. 
    It allows you to switch between different features and analysis sections with ease.
    """)

# Footer
st.markdown("""
---
Created with ❤️ by [Minh Hung](https://www.linkedin.com/in/nmh7/).
""")