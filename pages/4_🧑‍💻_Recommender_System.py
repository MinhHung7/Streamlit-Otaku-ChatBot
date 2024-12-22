import streamlit as st
import pandas as pd
import plotly.express as px
import io
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Recommender System", page_icon="🧑‍💻")

st.title("Anime Recommender System")

if 'csv_file' in st.session_state:

    # Read the CSV from session state into DataFrame
    df = pd.read_csv(io.StringIO(st.session_state.csv_file))

    # Header Section
    st.title('Anime Recommender System')
    st.markdown("""
    Welcome to the **Anime Recommender System**! 🎬🍿
    Just type the name of an anime below, and we’ll recommend similar ones based on genre, rating, and specialty score.
    """)

    columns_to_be_dropped = ['Score', 'Synopsis', 'Rank', 'Popularity', 'Favorites', 'Scored By', 'Members']
    df.drop(columns=columns_to_be_dropped, inplace=True)

    df['Released date'] = pd.to_datetime(df['Released date'], errors='coerce')
    df['Completed date'] = pd.to_datetime(df['Completed date'], errors='coerce')

    # Drop the 'Producers' column
    df.drop(columns=['Producers'], inplace=True)

    # Drop các sample có giá trị 'UNKNOWN' trong 'Studios' và 'Source'
    mask = df['Studios'].str.upper().str.contains('UNKNOWN') | df['Source'].str.upper().str.contains('UNKNOWN')
    df = df[~mask]
    df = df.reset_index(drop=True)


    type_dummies = df['Type'].str.get_dummies()
    source_dummies = df['Source'].str.get_dummies()

    # Thêm dữ liệu mới tạo vào df cũ
    df = pd.concat([df, type_dummies, source_dummies], axis=1)

    # Drop các cột 'Type', 'Source' sau khi đã tạo dummies
    df.drop(columns=['Type', 'Source'], inplace=True)

    encoder = LabelEncoder()
    df['Rating'] = encoder.fit_transform(df['Rating'])

    df['Genres'] = df['Genres'].apply(lambda x: [x.strip() for x in x.split(',')])
    df['Genres'] = df['Genres'].apply(lambda x: x if isinstance(x, list) else [])
    df['Studios'] = df['Studios'].apply(lambda x: [x.strip() for x in x.split(',')])

    # Sử dụng mulitlabel binarizer của sklearn
    mlbinarizer = MultiLabelBinarizer()


    # Feature Studios
    # fit_transform cột Studios thành một ma trận nhị phân
    altered_Studios_matrix = mlbinarizer.fit_transform(df['Studios'])
    # Chuyển ma trận đó thành DataFrame
    altered_Studios_df = pd.DataFrame(altered_Studios_matrix, columns=mlbinarizer.classes_)
    # Gắn dataframe mới vào dataframe cũ
    df = pd.concat([df, altered_Studios_df], axis=1)


    mlbinarizer = MultiLabelBinarizer()
    # Feature Genres
    # fit_transform cột Genres thành một ma trận nhị phân
    altered_Genres_matrix = mlbinarizer.fit_transform(df['Genres'])
    # Chuyển ma trận đó thành DataFrame
    altered_Genres_df = pd.DataFrame(altered_Genres_matrix, columns=mlbinarizer.classes_)
    # Gắn dataframe mới vào dataframe cũ
    df = pd.concat([df, altered_Genres_df], axis=1)
    
    df.drop(columns=['Genres', 'Studios'], inplace=True)


    df['Released date'] = df['Released date'].dt.year

    df['Completed date'] = df['Completed date'].dt.year
    df['Completed date'] = df['Completed date'].fillna(2023)

    # Chuyển về kiểu int cho đồng bộ
    df['Released date'] = df['Released date'].astype(int)
    df['Completed date'] = df['Completed date'].astype(int)

    # Các cột cần chuẩn hóa
    numeric_features = ['Episodes', 'Time per ep (Min)', 'Released date', 'Completed date']

    # Tạo scaler
    scaler = StandardScaler()

    # Chuẩn hóa các cột số
    df[numeric_features] = scaler.fit_transform(df[numeric_features])


    anime_info_df = df.drop(columns='Name')
    cosine_similarity_matrix = cosine_similarity(anime_info_df, anime_info_df)

    def recommend_anime(anime_name, top_n=10):

        # Find the index of the input anime
        input_anime_sample = df[df['Name'].str.contains(anime_name, case=False, na=False)]

        if input_anime_sample.empty:
            st.write('Sorry, we couldn\'t find that anime in our database. Please try again with a different name.')
            return
        
        input_anime_index = input_anime_sample.index[0]

        # Calculate cosine similarity
        similarities = list(enumerate(cosine_similarity_matrix[input_anime_index]))
        similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
        
        # Get top N anime recommendations
        top_n_anime = similarities[1:top_n+1]
        # Lấy tên của top N bộ anime
        top_n_anime_index = [anime[0] for anime in top_n_anime]
        top_n_anime_names = df.iloc[top_n_anime_index]['Name']

        # Display top N recommendations
        st.write(f"### Top {top_n} Anime you might like if you like '{anime_name}':")
        for i, anime_names in enumerate(top_n_anime_names):
            st.write(f"{i+1}. {anime_names}")

        # Plotting the recommendation scores
        top_n_scores = [similarities[i][1] for i in range(1, top_n+1)]
        fig = px.bar(
            x=top_n_anime_names,
            y=top_n_scores,
            labels={'x': 'Anime Name', 'y': 'Cosine Similarity Score'},
            title=f"Top {top_n} Recommendations for '{anime_name}'"
        )
        st.plotly_chart(fig)

    # Sidebar for user input
    st.sidebar.header('User Input')

    # Anime name input
    selected_anime = st.sidebar.text_input('Enter Anime Name', '')

    if selected_anime:
        recommend_anime(selected_anime)
    else:
        st.write("Please enter an anime name to get recommendations.")

    # Footer
    st.markdown("""
    ---
    Created with ❤️ by Minh Hung.
    """)

else:
    st.write("Please create and download a CSV first!")
