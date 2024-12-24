import streamlit as st
import pandas as pd
import io
from streamlist_pandas import filter_string, create_widgets, filter_df
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import datetime as dt

# Set the page title
st.set_page_config(page_title="Data Exploring", page_icon="📊", layout="wide")

# Title of the page
st.title("Data Exploring")

if 'csv_file' in st.session_state:

    st.markdown("""The **Data Exploring** page is where you dive deep into the anime dataset with clarity and precision. Here, you'll discover key statistics such as the number of anime, popular genres, and average ratings. Interactive visualizations, including bar charts, pie charts, heatmaps, and scatter plots, make it easy to grasp essential insights. With smart filters, you can quickly search by release year, genre, studio, or rating. This page not only helps you understand the data but also reveals hidden trends and relationships between factors, empowering you to make informed decisions for the next steps.""")
    st.markdown("""🚀 **Start your journey into anime data exploration today!**  """)

    # Read the CSV from session state into DataFrame
    df = pd.read_csv(io.StringIO(st.session_state.csv_file))
    
    overview_expander = st.expander("Overview of original anime dataset")

    # Display the DataFrame
    overview_expander.write(df)

    ###########################################
    st.sidebar.title("Control Panel")

    create_data = {}  # define this as needed, e.g. {'column_name': 'multiselect'}
    ignore_columns = []  # You can ignore specific columns if necessary
    all_widgets = create_widgets(df, create_data=create_data, ignore_columns=ignore_columns)

    # Step 4: Apply filtering based on user input from sidebar
    filtered_df = filter_df(df, all_widgets)
    
    #############################################
    # Genres handling
    filtered_df['Genres'] = filtered_df['Genres'].str.split(', ')
    filtered_df['Producers'] = filtered_df['Producers'].str.split(', ')
    filtered_df['Studios'] = filtered_df['Studios'].str.split(', ')
    ##########################################################

    basic_statistic_expander = st.expander("Data Statistic")
    numeric_cols = filtered_df.select_dtypes(exclude=['object', 'datetime64[ns]']).columns
    num_col_dist_df = filtered_df[numeric_cols].copy()
    missing_percentage = num_col_dist_df.isna().mean() * 100

    num_col_dist_df = num_col_dist_df.describe(percentiles=[.25, .5, .75]).round(2)
    num_col_dist_df.loc['missing ratios'] = missing_percentage
    basic_statistic_expander.dataframe(num_col_dist_df, use_container_width=True)

    ############################################
    
    with st.container(border=True):
        st.header("Distributions of Score and Popularity")
        # Define columns and colors
        col = ['Score', 'Popularity']
        color = ["#11264e", "#6faea4"]

        # Create Plotly figure for Score and Popularity histograms
        fig = make_subplots(rows=1, cols=2, shared_yaxes=True, column_widths=[0.5, 0.5], subplot_titles=["Distribution of Score", "Distribution of Popularity"])

        # Add histograms to each subplot (score and popularity)
        fig.add_trace(go.Histogram(x=filtered_df['Score'], name='Score', marker_color=color[0], opacity=0.75, nbinsx=100), row=1, col=1)
        fig.add_trace(go.Histogram(x=filtered_df['Popularity'], name='Popularity', marker_color=color[1], opacity=0.75, nbinsx=50), row=1, col=2)

        # Update layout to improve visuals
        fig.update_layout(
            title_text="",
            title_x=0.5,
            showlegend=False,
            xaxis_title="Score",
            yaxis_title="Count",
            xaxis2_title="Popularity",
            yaxis2_title="Count",
            template="plotly_white",
            height=500,  # Adjust the height if needed
            bargap=0.2,
            xaxis=dict(title_font=dict(size=15, weight='bold')),
            yaxis=dict(title_font=dict(size=15, weight='bold')),
            xaxis2=dict(title_font=dict(size=15, weight='bold')),
            yaxis2=dict(title_font=dict(size=15, weight='bold')),
        )

        # Show the Plotly chart in Streamlit
        st.plotly_chart(fig)
  
    ############################################

    with st.container(border=True):
        st.header("Distributions of Episodes and Time per Episode")
        # Define columns and colors
        col = ['Episodes', 'Time per ep (Min)']
        color = ["#00507A", "#11264e"]

        # Create Plotly figure for Episodes and Time per episode histograms
        fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], subplot_titles=["Distribution of Episodes (log scale)", "Distribution of Time per Episode (log scale)"])

        # Add histograms to each subplot (episodes and time per episode)
        fig.add_trace(go.Histogram(x=np.log10(filtered_df['Episodes'] + 1), name='Episodes', marker_color=color[0], opacity=0.75, marker=dict(
                line=dict(
                    color='black',  # Viền màu đen
                    width=2  # Độ dày của viền
                )
            )), row=1, col=1)
        fig.add_trace(go.Histogram(x=np.log10(filtered_df['Time per ep (Min)'] + 1), name='Time per ep (Min)', marker_color=color[1], opacity=0.75, marker=dict(
                line=dict(
                    color='black',  # Viền màu đen
                    width=2  # Độ dày của viền
                )
            )), row=1, col=2)

        # Apply logarithmic scale to the x-axis
        fig.update_layout(
            title_text="",
            showlegend=False,
            xaxis_title="Episodes",
            yaxis_title="Count",
            xaxis2_title="Time per Episode (Min)",
            yaxis2_title="Count",
            template="plotly_white",
            height=500,  # Adjust the height if needed
            bargap=0,
            xaxis=dict(title_font=dict(size=15, weight='bold')),
            yaxis=dict(title_font=dict(size=15, weight='bold')),
            xaxis2=dict(title_font=dict(size=15, weight='bold')),
            yaxis2=dict(title_font=dict(size=15, weight='bold')),
            
        )

        # Show the Plotly chart in Streamlit
        st.plotly_chart(fig)

    ########################################

    with st.container(border=True):
        st.header("Distributions of Scored By, Members, Favorites and Rank")

        col = ['Scored By', 'Members', 'Favorites', 'Rank']
        color = ['#a1c9f4', '#8de5a1', '#ff9f9b', '#d0bbff']

        fig = make_subplots(rows=1, cols=4, subplot_titles=["Distribution of Scored By", "Distribution of Members", "Distribution of Favorites", "Distribution of Rank"])

        for i in range(4):
            valid_data = filtered_df[col[i]].replace([np.inf, -np.inf], np.nan).dropna()
            valid_data = valid_data[valid_data > 0]
            
            fig.add_trace(
                go.Histogram(
                    x=np.log(valid_data),
                    marker=dict(color=color[i]),
                    nbinsx=100
                ),
                row=1, col=i+1
            )
            
            fig.update_xaxes(title_text=col[i], row=1, col=i+1)
            fig.update_yaxes(title_text='Count', row=1, col=i+1)

        fig.update_layout(
            title_text="",
            showlegend=False,
            bargap=0.2,
            height=500,
            width=1200,
            xaxis=dict(title_font=dict(size=15, weight='bold')),
            yaxis=dict(title_font=dict(size=15, weight='bold')),
        )

        # Display Plotly Chart in Streamlit
        st.plotly_chart(fig)

    #########################################################
    with st.container(border=True):
        st.header("Distributions of Original Source")

        # Lọc bỏ các giá trị 'Unknown' trong cột 'Source'
        filtered_anime_sources = filtered_df[filtered_df['Source'] != 'Unknown']

        # Lấy dữ liệu tần suất cho các nguồn
        sources = filtered_anime_sources['Source'].value_counts()

        # Màu sắc cho biểu đồ
        color = ["#11264e", "#00507A", "#026e90", "#008b99", "#6faea4", 
                "#fcdcb0", "#FEE08B", "#faa96e", "#f36b3b", "#ef3f28", "#CC0028"]

        # Tạo biểu đồ: Distribution of Original Source bằng Plotly
        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=sources.index,  # Các nhãn trên trục Y (là các nguồn)
            x=sources.values,  # Các giá trị (tần suất của mỗi nguồn)
            orientation='h',  # Horizontal bar chart
            marker=dict(color=color[:len(sources)], line=dict(color='black', width=2)),  # Màu sắc và viền
            name='Source',  # Tên biểu đồ
        ))

        # Cài đặt tiêu đề và nhãn
        fig.update_layout(
            title='',  # Tiêu đề của biểu đồ
            xaxis_title='Count',  # Tiêu đề trục X
            yaxis_title='Source',  # Tiêu đề trục Y
            template='plotly_white',  # Dùng nền trắng
            title_font=dict(size=20, color='black', family='Arial', weight='bold'),
            xaxis=dict(title_font=dict(size=15, weight='bold')),
            yaxis=dict(title_font=dict(size=15, weight='bold')),
            yaxis_autorange='reversed',  # Đảo ngược trục Y để giá trị lớn nhất ở trên
            margin=dict(l=100, r=20, t=40, b=60),  # Điều chỉnh các lề cho phù hợp
        )

        # Hiển thị biểu đồ trong Streamlit
        st.plotly_chart(fig)

    #################################################################

    with st.container(border=True):
        st.header("Distribution of Anime Type and Rating")

        # Lấy tần suất cho các cột 'Type' và 'Rating'
        type_counts = filtered_df['Type'].value_counts()
        rating_counts = filtered_df['Rating'].value_counts()

        # Màu sắc cho biểu đồ tròn
        type_colors = ['#ff9f9b', '#fffea3', '#d0bbff']
        rating_colors = ['#a1c9f4', '#8de5a1', '#8e35a1']

        # Tạo subplot với 1 hàng và 2 cột
        fig = make_subplots(
            rows=1, cols=2, 
            subplot_titles=['Distribution of Anime Type', 'Distribution of Anime Rating'],
            specs=[[{'type': 'pie'}, {'type': 'pie'}]]  # Cả hai biểu đồ là pie chart
        )

        # Thêm biểu đồ tròn cho 'Type'
        fig.add_trace(go.Pie(
            labels=type_counts.index,
            values=type_counts.values,
            name='Type',
            hoverinfo='label+percent',
            textinfo='percent',
            textfont=dict(size=14),
            marker=dict(colors=type_colors, line=dict(color='black', width=2)),
            showlegend=True
        ), row=1, col=1)

        # Thêm biểu đồ tròn cho 'Rating'
        fig.add_trace(go.Pie(
            labels=rating_counts.index,
            values=rating_counts.values,
            hoverinfo='label+percent',
            name='Rating',
            textinfo='percent',
            textfont=dict(size=14),
            marker=dict(colors=rating_colors, line=dict(color='black', width=2)),
            showlegend=True
        ), row=1, col=2)

        # Cập nhật layout của subplot
        fig.update_layout(
            title='',
            title_x=0.5,
            title_font=dict(size=18, weight='bold'),
            height=500,  # Chiều cao của biểu đồ
            showlegend=True,  # Tắt legend chung, mỗi biểu đồ sẽ có legend riêng
            legend=dict(
                font=dict(size=10),
                orientation='h',  # Hiển thị legend theo chiều ngang
                yanchor='bottom', y=1.1, xanchor='center', x=0.5
            ),
            margin=dict(t=50, b=50, l=50, r=50),  # Điều chỉnh các lề
        )

        # Hiển thị biểu đồ trong Streamlit
        st.plotly_chart(fig)

    ################################################################
    with st.container(border=True):

        # Trực quan hóa phân phối của Genres
        genres = filtered_df['Genres'].explode()
        genres_counts = genres.value_counts().head(10)  # Lấy 10 Genres phổ biến nhất

        # Màu sắc cho các biểu đồ
        colors = ['#ff9f9b', '#fffea3', '#d0bbff', '#a1c9f4', '#8de5a1', '#8e35a1', '#f36b3b', '#ef3f28', '#008b99', '#6faea4']

        # Tạo subplot với 1 hàng và 1 cột cho 1 biểu đồ
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{'type': 'bar'}]]  # Biểu đồ là bar chart
        )

        # Thêm biểu đồ cho 'Genres'
        fig.add_trace(go.Bar(
            x=genres_counts.values,
            y=genres_counts.index,
            orientation='h',
            marker=dict(
                color=colors[:len(genres_counts)],  # Màu cho các thanh
                line=dict(
                    color='black',  # Viền màu đen
                    width=2  # Độ dày của viền
                )
            ),
            name='Genres',
        ))

        # Cập nhật layout của subplot
        fig.update_layout(
            title_text='',  # Tiêu đề của biểu đồ
            title_x=0.5,  # Căn giữa tiêu đề
            title_font=dict(size=20, weight='bold'),  # Chữ in đậm cho tiêu đề
            height=600,  # Chiều cao của biểu đồ
            margin=dict(t=50, b=50, l=50, r=50),  # Điều chỉnh các lề
        )

        # Cập nhật các trục x và y
        fig.update_xaxes(
            title_text="Count", 
            tickfont=dict(size=12), 
            title_font=dict(weight="bold")
        )
        fig.update_yaxes(
            title_text="Genres", 
            tickfont=dict(size=12), 
            title_font=dict(weight="bold")
        )

        # Hiển thị biểu đồ trong Streamlit
        st.header("Distribution of Genres")  # Thêm tiêu đề trong Streamlit
        st.plotly_chart(fig)  # Vẽ biểu đồ trong Streamlit

    ###########################################################
else:
    st.write("Please create and download a CSV first!")


