import streamlit as st
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from streamlist_pandas import filter_string, create_widgets, filter_df
import pandas as pd
import io
import datetime as dt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

st.set_page_config(page_title="Problems Solving", page_icon="💬")

st.title("Data-driven Insights into Anime 2023")

if 'csv_file' in st.session_state:

    # Read the CSV from session state into DataFrame
    df = pd.read_csv(io.StringIO(st.session_state.csv_file))

    ############################################################
    st.sidebar.title("Control Panel")

    create_data = {}  # define this as needed, e.g. {'column_name': 'multiselect'}
    ignore_columns = []  # You can ignore specific columns if necessary
    all_widgets = create_widgets(df, create_data=create_data, ignore_columns=ignore_columns)

    # Step 4: Apply filtering based on user input from sidebar
    filtered_df = filter_df(df, all_widgets)
    ############################################################
    # Genres handling
    filtered_df['Genres'] = filtered_df['Genres'].str.split(', ')
    filtered_df['Producers'] = filtered_df['Producers'].str.split(', ')
    filtered_df['Studios'] = filtered_df['Studios'].str.split(', ')
    ##########################################################

    # Create a container for the cards
    st.header("Questions")

    # Create columns for cards
    question_col1, question_col2, question_col3 = st.columns(3)

    # Card 1
    with question_col1:
        col1_expander = question_col1.expander("Question 1")
        col1_expander.markdown("**Câu hỏi:**")
        col1_expander.write("Số lượng anime được phát hành thay đổi như thế nào theo các mùa khác nhau trong năm? Có xu hướng rõ ràng nào trong việc phân phối các bản phát hành anime theo mùa không?")
        col1_expander.markdown("**Mục đích:**")
        col1_expander.markdown("- Tìm hiểu sâu hơn về chu kỳ phát hành anime, khám phá xu hướng phát hành anime.")
        col1_expander.markdown("- Cung cấp thông tin có giá trị cho các nhà xuất bản, độc giả và các chuyên gia trong ngành để lập kế hoạch, chiến lược tiếp thị và ra quyết định sáng suốt.")

        question_col1_solving_button = col1_expander.button("Problem 1 Solving")
    # Card 2
    with question_col2:
        col2_expander = question_col2.expander("Question 2")
        col2_expander.write("Những thể loại anime nào được đánh giá là nổi bật nhất dựa trên một điểm số tổng hợp, tính từ các yếu tố như số lượt yêu thích trung bình, số lượng anime, điểm đánh giá trung bình và độ phổ biến?")
        col2_expander.markdown("**Mục đích:**")
        col2_expander.markdown("- Xác định và xếp hạng các thể loại anime dựa trên điểm tổng hợp từ các yếu tố như số lượng yêu thích trung bình, số lượng anime trong mỗi thể loại, điểm trung bình và mức độ phổ biến.")
        col2_expander.markdown("- Cung cấp cái nhìn toàn diện về các thể loại anime bằng cách kết hợp nhiều số liệu, cung cấp thông tin chi tiết về các thể loại vượt trội trên nhiều tiêu chí khác nhau.")

        question_col2_solving_button = col2_expander.button("Problem 2 Solving")
    # Card 3
    with question_col3:
        col3_expander = question_col3.expander("Question 3")
        col3_expander.write("Mối quan hệ cân bằng tối ưu giữa số tập, thời lượng mỗi tập và lịch phát hành để tối đa hóa cả lượt xem và đánh giá phê bình là gì?")
        col3_expander.markdown("**Mục đích:**")
        col3_expander.markdown("- Xác định điểm cân bằng trong các lựa chọn sản xuất giúp cân bằng hiệu quả chi phí với sự hài lòng và tương tác của khán giả.")

        question_col3_solving_button = col3_expander.button("Problem 3 Solving")
    # Create columns for cards
    question_col4, question_col5 = st.columns(2)

    # Card 4
    with question_col4:
        col4_expander = question_col4.expander("Question 4")
        col4_expander.write("Sự hợp tác giữa nhà sản xuất và studio ảnh hưởng như thế nào đến hiệu suất và sự đón nhận của anime, và những mối quan hệ đối tác nào trong lịch sử là thành công nhất?")
        col4_expander.markdown("**Mục đích:**")
        col4_expander.markdown("- Phân tích các sự hợp tác có thể khám phá ra những sự kết hợp thành công giữa các studio và nhà sản xuất, cho phép các nhà sản xuất phim hình thành các mối quan hệ đối tác chiến lược nhằm tối đa hóa chất lượng và sự hấp dẫn đối với khán giả.")

        question_col4_solving_button = col4_expander.button("Problem 4 Solving")
    # Card 5
    with question_col5:
        col5_expander = question_col5.expander("Question 5")
        col5_expander.write("Mỗi thể loại anime thường gắn liền với những studio nổi bật trong việc sản xuất, vậy đâu là studio sở trường của từng thể loại anime?")
        col5_expander.markdown("**Mục đích:**")
        col5_expander.markdown("- Một studio có kinh nghiệm và thành tích tốt trong một thể loại anime cụ thể sẽ cho ra các sản phẩm có chất lượng tốt hơn, góp phần đảm bảo được sự thành công của bộ anime đó. Việc biết được studio nào có sở trường trong thể loại nào sẽ giúp nhà sản xuất đưa ra quyết định phù hợp.")

        question_col5_solving_button = col5_expander.button("Problem 5 Solving")

    if question_col1_solving_button:
        st.markdown("---")
        st.markdown("### Số lượng anime được phát hành thay đổi như thế nào theo các mùa khác nhau trong năm? Có xu hướng rõ ràng nào trong việc phân phối các bản phát hành anime theo mùa không?")

        df_copy = filtered_df.copy()

        df_copy['Released date'] = pd.to_datetime(df_copy['Released date'], errors='coerce')

        df_copy['Month'] = df_copy['Released date'].dt.month.astype('int64')
        df_copy['Year'] = df_copy['Released date'].dt.year.astype('int64')
        df_copy['Decade'] = df_copy['Year'] // 10 * 10
        seasons = ['Winter', 'Spring', 'Summer', 'Fall']
        df_copy['Season'] = pd.cut(df_copy['Month'], [0, 3, 6, 9, 12], labels=seasons, include_lowest=True)

        anime_per_season = df_copy[df_copy['Year'] >= 1990].groupby(['Decade', 'Season']).size().reset_index(name='Count')
        anime_per_season['Percentage'] = anime_per_season['Count'] / anime_per_season.groupby('Decade')['Count'].transform('sum') * 100


        fig_area = go.Figure()

        # Group by 'Decade' and 'Season' for percentage
        for season in anime_per_season['Season'].unique():
            season_data = anime_per_season[anime_per_season['Season'] == season]
            fig_area.add_trace(go.Scatter(
                x=season_data['Decade'],
                y=season_data.groupby('Decade')['Percentage'].sum(),
                mode='lines',
                stackgroup='one',
                name=season
            ))

        # Customize the layout for the area plot
        fig_area.update_layout(
            title="Percentage of Anime Released Per Season Per Decade",
            xaxis_title="Decade",
            yaxis_title="Percentage",
            template="plotly",
            showlegend=True,
            legend_title="Seasons",
            height=500,
            xaxis=dict(
                tickvals=list(range(1990, 2030, 10)),  # Convert range to list
                ticktext=[str(i) for i in range(1990, 2030, 10)],  # Label for each tick
            )
        )

        # 2. Stacked Bar Plot for Number of Anime Released per Season per Decade
        fig_bar = go.Figure()

        # Group by 'Decade' and 'Season' for count
        for season in anime_per_season['Season'].unique():
            season_data = anime_per_season[anime_per_season['Season'] == season]
            fig_bar.add_trace(go.Bar(
                x=season_data['Decade'],
                y=season_data.groupby('Decade')['Count'].sum(),
                name=season,
                text=season_data.groupby('Decade')['Count'].sum(),
                textposition='inside',
            ))

        # Customize the layout for the bar plot
        fig_bar.update_layout(
            title="Number of Anime Released Per Season Per Decade",
            xaxis_title="Decade",
            yaxis_title="Number of Anime",
            template="plotly",
            showlegend=True,
            legend_title="Seasons",
            barmode='stack',
            height=500,
        )

        # Create two columns to display the plots side by side
        bar_col1, bar_col2 = st.columns(2)

        # Display the first plot (Stacked Area Plot) in the first column
        with bar_col1:
            st.plotly_chart(fig_area)

        # Display the second plot (Stacked Bar Plot) in the second column
        with bar_col2:
            st.plotly_chart(fig_bar)

        st.markdown("""**Câu hỏi**
- Những thể loại anime nào được đánh giá là nổi bật nhất dựa trên một điểm số tổng hợp, tính từ các yếu tố như số lượt yêu thích trung bình, số lượng anime, điểm đánh giá trung bình và độ phổ biến?

**Mục đích**
- Xác định và xếp hạng các thể loại anime dựa trên điểm tổng hợp từ các yếu tố như số lượng yêu thích trung bình, số lượng anime trong mỗi thể loại, điểm trung bình và mức độ phổ biến.
- Cung cấp cái nhìn toàn diện về các thể loại anime bằng cách kết hợp nhiều số liệu, cung cấp thông tin chi tiết về các thể loại vượt trội trên nhiều tiêu chí khác nhau.

**Phân tích**
- Mở rộng tập dữ liệu để mỗi thể loại được hiển thị thành một dòng riêng với thông tin chi tiết về manga.  
- Nhóm dữ liệu theo thể loại và tính toán:  
    - Số lượt yêu thích trung bình theo từng thể loại.  
    - Số lượng manga theo từng thể loại.  
    - Điểm trung bình theo từng thể loại.  
    - Độ phổ biến trung bình theo từng thể loại.  
- Tạo một điểm tổng hợp được kết hợp từ các chỉ số này.  
- Xếp hạng các thể loại dựa trên điểm tổng hợp trên và hiển thị các thể loại hàng đầu.    """)
        

    if question_col2_solving_button:
        st.markdown("---")
        st.markdown("### Những thể loại anime nào được đánh giá là nổi bật nhất dựa trên một điểm số tổng hợp, tính từ các yếu tố như số lượt yêu thích trung bình, số lượng anime, điểm đánh giá trung bình và độ phổ biến?")

        anime_copy_df = filtered_df.copy()

        # Phân tách tập dữ liệu để mỗi thể loại có một hàng riêng với các chi tiết về anime
        exploded_data_by_genre = anime_copy_df.explode('Genres')

        # Nhóm dữ liệu theo thể loại và tính toán các số liệu cần thiết cho từng thể loại
        genre_grouped = exploded_data_by_genre.groupby('Genres').agg({
            'Favorites': 'mean',  # Average favorite count
            'Score': 'mean',     # Average score
            'Name': 'count',    # Number of anime
            'Popularity': 'mean' # Average popularity
        }).reset_index()

        # Tạo điểm tổng hợp (điểm trung bình đơn giản của điểm chuẩn hóa của bốn số liệu)
        scaler = MinMaxScaler()
        genre_grouped[['Favorites_norm', 'Score_norm', 'Name_count', 'Popularity_norm']] = scaler.fit_transform(
            genre_grouped[['Favorites', 'Score', 'Name', 'Popularity']]
        )

        genre_grouped['Composite_Score'] = genre_grouped[['Favorites_norm', 'Score_norm', 'Name_count', 'Popularity_norm']].mean(axis=1)

        sorted_by_composite_score = genre_grouped.sort_values(by='Composite_Score', ascending=False)

        top_genres_by_composite_score = sorted_by_composite_score.head(10)

        # Define the custom color palette
        palette = ["#11264e", "#00507A", "#026e90", "#008b99", "#6faea4", "#fcdcb0", "#FEE08B", "#faa96e", "#f36b3b", "#ef3f28", "#CC0028"]

        # Create a Plotly bar plot
        fig = px.bar(
            top_genres_by_composite_score,
            x='Composite_Score',
            y='Genres',
            color='Genres',  # This will use different colors for each genre
            color_discrete_sequence=palette,  # Apply the custom color palette
            title="Top 10 Anime Genres by Composite Score",
            labels={'Composite_Score': 'Composite Score', 'Genres': 'Genre'},
            template="plotly",
        )

        # Customize layout
        fig.update_layout(
            title={
                'text': "Top 10 Anime Genres by Composite Score",
                'x': 0.5,  # Center the title
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 30, 'family': 'Arial'}
            },
            xaxis={
                'title': 'Composite Score',
                'title_font': {'size': 20, 'family': 'Arial'},
                'tickfont': {'size': 17}
            },
            yaxis={
                'title': 'Genre',
                'title_font': {'size': 20, 'family': 'Arial'},
                'tickfont': {'size': 17}
            },
            showlegend=False  # Hide the legend as it might not be needed
        )

        # Show plot in Streamlit
        st.plotly_chart(fig)

        st.markdown("""**Nhận xét**

    - *Award Winning* là thể loại đứng đầu bảng xếp hạng, cho thấy các bộ anime trong danh mục này không chỉ nhận được nhiều lời khen ngợi mà còn đạt sự yêu thích cao của độc giả và đánh giá tốt từ giới phê bình.  
    - *Comedy* và *Action* xếp ngay sau, cho thấy độc giả có xu hướng ưa chuộng những chủ đề này, có thể do tính phổ biến và khả năng đa dạng trong cách kể chuyện của chúng.  
    - *Suspense* và *Fantasy* cũng đạt điểm số cao, phù hợp với xu hướng toàn cầu khi hai thể loại này có lượng fan đông đảo và số lượng tác phẩm lớn.  
    - Các thể loại như *Adventure*, *Drama*, và *Sci-Fi* giữ vị trí trung bình về độ phổ biến. Những thể loại này thường có sự kết hợp trong các nguyên tác cũng như trong các bộ anime, cho thấy sự pha trộn này phù hợp với thị hiếu của khán giả.  
    - *Romance* và *Supernatural* nằm ở cuối trong top 10, có thể do lượng khán giả của hai thể loại này thuộc nhóm đối tượng nhỏ hơn hoặc số lượng tác phẩm ít hơn so với các thể loại khác.  """)
            
    if question_col3_solving_button:
        st.markdown("---")
        st.markdown("### Mối quan hệ cân bằng tối ưu giữa số tập, thời lượng mỗi tập và lịch phát hành để tối đa hóa cả lượt xem và đánh giá phê bình là gì?")

        clean_filtered_df = filtered_df[['Episodes', 'Time per ep (Min)', 'Score' ,'Scored By', 'Popularity', 'Rank']]
        clean_filtered_df['Total Duration'] = clean_filtered_df['Time per ep (Min)'] * clean_filtered_df['Episodes']

        # Tính toán ma trận tương quan giữa các cột có liên quan
        correlation_matrix = clean_filtered_df[['Episodes', 'Time per ep (Min)', 'Total Duration', 'Score', 'Scored By', 'Popularity', 'Rank']].corr()

        # Create a heatmap using Plotly
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,  # Extract the NumPy array for the correlation values
            x=correlation_matrix.columns,  # Set the column names as x-axis labels
            y=correlation_matrix.columns,  # Set the column names as y-axis labels
            colorscale='RdBu',  # Use the 'RdBu' colorscale (or choose any available colorscale)
            colorbar=dict(title="Correlation", tickvals=[-1, 0, 1], ticktext=["-1", "0", "1"]),
            zmin=-1, zmax=1,  # Set the min and max range for correlation values
            text=correlation_matrix.round(2).values,  # Use rounded values for displaying in cells
            texttemplate="%{text}",  # Display the text as it is (no formatting)
        ))

        # Update layout for the heatmap
        fig.update_layout(
            title="Correlation Matrix",
            title_x=0.5,  # Center the title
            xaxis=dict(title='Variables', tickvals=np.arange(len(correlation_matrix.columns)), ticktext=correlation_matrix.columns),
            yaxis=dict(title='Variables', tickvals=np.arange(len(correlation_matrix.columns)), ticktext=correlation_matrix.columns),
            xaxis_title_font=dict(size=14, color='black'),
            yaxis_title_font=dict(size=14, color='black'),
            font=dict(size=14),
            plot_bgcolor="white",  # Optional: Set plot background to white
        )

        # Display the heatmap in Streamlit
        st.plotly_chart(fig)

        st.markdown("""**Nhận xét**
    - Chất lượng không đồng nghĩa với sự phổ biến: Một anime có điểm số cao không nhất thiết phải là một anime được nhiều người xem. Có thể một số anime chất lượng cao (theo đánh giá của người xem) nhưng lại không được biết đến rộng rãi hoặc không thu hút đông đảo khán giả.

    - Phổ biến không đồng nghĩa với chất lượng: Các anime phổ biến có thể không phải lúc nào cũng có chất lượng đánh giá tốt. Đôi khi, anime được nhiều người xem không phải vì nó hay, mà vì nó dễ tiếp cận hoặc vì lý do marketing, tên tuổi, hoặc thương hiệu.

    - Vì `Popularity` có mối tương quan dương mạnh với `Rank`, nên sẽ giữ lại thuộc tính `Popularity`, không xét thuộc tính `Score`""")
            
        # Create the subplots with 2 rows and 3 columns
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=(
                "Popularity vs Episodes",
                "Popularity vs Time per ep (Min)",
                "Popularity vs Total Duration",
                "Popularity vs Episodes (Zoomed In)",
                "Popularity vs Time per ep (Min) (Zoomed In)",
                "Popularity vs Total Duration (Zoomed In)"
            ),
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )

        # Plot Popularity vs Episodes (Top Left)
        fig.add_trace(go.Scatter(
            x=clean_filtered_df['Episodes'], y=clean_filtered_df['Popularity'], mode='markers', name='Popularity vs Episodes'
        ), row=1, col=1)

        # Plot Popularity vs Time per Episode (Top Middle)
        fig.add_trace(go.Scatter(
            x=clean_filtered_df['Time per ep (Min)'], y=clean_filtered_df['Popularity'], mode='markers', name='Popularity vs Time per ep (Min)'
        ), row=1, col=2)

        # Plot Popularity vs Total Duration (Top Right)
        fig.add_trace(go.Scatter(
            x=clean_filtered_df['Total Duration'], y=clean_filtered_df['Popularity'], mode='markers', name='Popularity vs Total Duration'
        ), row=1, col=3)

        # Plot Popularity vs Episodes (Zoomed In) (Bottom Left)
        fig.add_trace(go.Scatter(
            x=clean_filtered_df['Episodes'], y=clean_filtered_df['Popularity'], mode='markers', name='Popularity vs Episodes (Zoomed In)'
        ), row=2, col=1)

        # Set the x-axis limits for the "zoomed in" plots
        fig.update_xaxes(range=[0, 100], row=2, col=1)

        # Plot Popularity vs Time per Episode (Zoomed In) (Bottom Middle)
        fig.add_trace(go.Scatter(
            x=clean_filtered_df['Time per ep (Min)'], y=clean_filtered_df['Popularity'], mode='markers', name='Popularity vs Time per ep (Min) (Zoomed In)'
        ), row=2, col=2)

        # Set the x-axis limits for the "zoomed in" plots
        fig.update_xaxes(range=[0, 100], row=2, col=2)

        # Plot Popularity vs Total Duration (Zoomed In) (Bottom Right)
        fig.add_trace(go.Scatter(
            x=clean_filtered_df['Total Duration'], y=clean_filtered_df['Popularity'], mode='markers', name='Popularity vs Total Duration (Zoomed In)'
        ), row=2, col=3)

        # Set the x-axis limits for the "zoomed in" plots
        fig.update_xaxes(range=[0, 2000], row=2, col=3)

        # Update layout
        fig.update_layout(
            title_text="Popularity vs Various Parameters",  # Overall title
            showlegend=False,  # Hide the legend
            height=900,  # Adjust the height of the plot
            title_x=0.5,  # Center the title
        )

        # Display the figure in Streamlit
        st.plotly_chart(fig)

        st.markdown("""**Nhận xét**
    - Các bộ anime không nhất thiết phải có số tập nhiều và thời lượng mỗi tập nhiều mới đạt được `Popularity` cao
    - Đa số các bộ anime có `Popularity` cao thì có số tập `Episodes` khoảng 60 tập và thời gian mỗi tập trong khoảng 0-40 phút""")
            
        inertia = []

        # Loop to compute inertia for k from 1 to 10
        for k in range(1, 11):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(clean_filtered_df[['Episodes', 'Time per ep (Min)', 'Popularity', 'Total Duration']])
            inertia.append(kmeans.inertia_)

        # Create the plot using Plotly
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=list(range(1, 11)),
            y=inertia,
            mode='lines+markers',
            name='Inertia',
            marker=dict(size=8, color='blue'),
            line=dict(color='blue', width=2)
        ))

        # Update layout for the plot
        fig.update_layout(
            title="Elbow Method for Optimal k",
            title_x=0.5,  # Center the title
            xaxis=dict(
                title='Number of Clusters (k)',
                tickvals=list(range(1, 11)),
                ticktext=list(range(1, 11)),
                showgrid=True
            ),
            yaxis=dict(
                title='Inertia',
                showgrid=True
            ),
            template="plotly_white",  # You can change the template style if needed
            font=dict(size=14),
            showlegend=False
        )

        # Display the figure in Streamlit
        st.plotly_chart(fig)

        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        clean_filtered_df['Cluster'] = kmeans.fit_predict(clean_filtered_df[['Episodes', 'Time per ep (Min)', 'Popularity', 'Total Duration']])

        # Create an empty string to store the cluster summaries
        cluster_summary = ""

        # Create 3 columns for displaying the clusters side-by-side
        col1, col2, col3 = st.columns(3)

        # Loop over each cluster and display descriptive statistics in 3 columns
        for i, cluster_num in enumerate(clean_filtered_df['Cluster'].unique()):
            cluster_data = clean_filtered_df[clean_filtered_df['Cluster'] == cluster_num]
            
            # Get the descriptive statistics as a DataFrame
            cluster_desc = cluster_data[['Popularity', 'Episodes', 'Time per ep (Min)', 'Total Duration']].describe()
            
            # Assign the statistics to the respective column
            if i == 0:
                with col1:
                    st.markdown(f"### Cluster {cluster_num}")
                    st.write(cluster_desc)
            elif i == 1:
                with col2:
                    st.markdown(f"### Cluster {cluster_num}")
                    st.write(cluster_desc)
            else:
                with col3:
                    st.markdown(f"### Cluster {cluster_num}")
                    st.write(cluster_desc)
        
        st.markdown("""**Nhận xét**

    - Phần lớn các anime trong dữ liệu này có số tập rất ít, từ 1 đến 5 tập (phân vị 25% đến 75% là 1 đến 5 tập). Điều này cho thấy rằng người xem có xu hướng chọn các anime ngắn, dễ tiếp cận và tiêu thụ trong thời gian ngắn.

    -> **Các nhà sản xuất nên cân nhắc sản xuất các chương trình hoặc series có khoảng 1 đến 5 tập, vì đây là số lượng tập phổ biến và dễ dàng thu hút người xem.**

    - Thời gian mỗi tập phần lớn dưới 30 phút (phân vị 75% là 26 phút), với một số tập cực kỳ ngắn (như chỉ 3 phút). Điều này cho thấy người xem có xu hướng thích các nội dung ngắn gọn, dễ tiêu thụ.

    -> **Để phù hợp với thói quen người dùng ngày nay, đặc biệt với sự phổ biến của các video trên mạng xã hội và các nền tảng phát trực tuyến, các anime có thời gian mỗi tập từ 10 đến 30 phút sẽ là lựa chọn lý tưởng. Điều này cho phép người xem dễ dàng theo dõi mà không mất quá nhiều thời gian.**

    ---
    """)


    if question_col4_solving_button:
        st.markdown("---")
        st.markdown("### Sự hợp tác giữa nhà sản xuất và studio ảnh hưởng như thế nào đến hiệu suất và sự đón nhận của anime, và những mối quan hệ đối tác nào trong lịch sử là thành công nhất?")

        clean_filtered_df = filtered_df[['Producers', 'Studios', 'Score', 'Popularity', 'Favorites', 'Type']]
        # Xóa các dòng nếu cả hai cột đều có giá trị 'UNKNOWN'
        clean_filtered_df = clean_filtered_df[~((clean_filtered_df['Studios'] == 'UNKNOWN') & (clean_filtered_df['Producers'] == 'UNKNOWN'))]

        # Thay thế 'UNKNOWN' bằng chuỗi rỗng nếu chỉ có một trong hai cột có giá trị 'UNKNOWN'
        clean_filtered_df['A'] = clean_filtered_df['Studios'].replace('UNKNOWN', '')
        clean_filtered_df['B'] = clean_filtered_df['Producers'].replace('UNKNOWN', '')

        # Convert Producers and Studios to string (handling cases where they are lists)
        clean_filtered_df['Producers'] = clean_filtered_df['Producers'].apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x))
        clean_filtered_df['Studios'] = clean_filtered_df['Studios'].apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x))

        clean_filtered_df['Producer-Studio'] = clean_filtered_df['Producers'] + ' - ' + clean_filtered_df['Studios']
        # Tính toán ma trận tương quan giữa các cột có liên quan
        correlation_matrix = clean_filtered_df.corr(numeric_only=True)

        # Create a heatmap using Plotly
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,  # Extract the NumPy array for the correlation values
            x=correlation_matrix.columns,  # Set the column names as x-axis labels
            y=correlation_matrix.columns,  # Set the column names as y-axis labels
            colorscale='RdBu',  # Use the 'RdBu' colorscale (or choose any available colorscale)
            colorbar=dict(title="Correlation", tickvals=[-1, 0, 1], ticktext=["-1", "0", "1"]),
            zmin=-1, zmax=1,  # Set the min and max range for correlation values
            text=correlation_matrix.round(2).values,  # Use rounded values for displaying in cells
            texttemplate="%{text}",  # Display the text as it is (no formatting)
        ))

        # Update layout for the heatmap
        fig.update_layout(
            title="Correlation Matrix",
            title_x=0.5,  # Center the title
            xaxis=dict(title='Variables', tickvals=np.arange(len(correlation_matrix.columns)), ticktext=correlation_matrix.columns),
            yaxis=dict(title='Variables', tickvals=np.arange(len(correlation_matrix.columns)), ticktext=correlation_matrix.columns),
            xaxis_title_font=dict(size=14, color='black'),
            yaxis_title_font=dict(size=14, color='black'),
            font=dict(size=14),
            plot_bgcolor="white",  # Optional: Set plot background to white
        )

        # Display the heatmap in Streamlit
        st.plotly_chart(fig)

        # Group by 'Producer-Studio' and calculate mean values for Score, and Favorites
        partnership_performance = clean_filtered_df.groupby('Producer-Studio')[['Score', 'Favorites']].mean()

        # Sort the results to find the best-performing partnerships
        partnership_performance = partnership_performance.sort_values(by='Score', ascending=False)

        # Filter the top 10 partnerships based on Score
        top_partnerships = partnership_performance.nlargest(10, 'Score')

        # Create the bar plot using Plotly Express
        fig = px.bar(
            top_partnerships,
            x=top_partnerships.index,  # Ensure 'Producer-Studio' is the column you want on the x-axis
            y='Score',
            title='Top 10 Producer-Studio Partnerships by Score',
            labels={'Producer-Studio': 'Producer-Studio Partnership', 'Score': 'Average Score'},
            color='Score',  # Color bars based on Score
            color_continuous_scale='Blues',  # Color scale for the bars
        )

        # Update layout for better visualization
        fig.update_layout(
            xaxis_tickangle=-45,  # Rotate x-axis labels for better visibility
            xaxis_title=None,  # Remove x-axis title
            yaxis_title='Average Score',  # Add y-axis title
            plot_bgcolor='white',  # Set background color
            template='plotly_white',  # Use a clean template for the plot
            height=1000,
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        st.markdown("""**Nhận xét**
    - `Sunrise` cùng với `Bandai Namco Pictures` là hai studio tham gia vào sản xuất nhiều bộ anime thuộc top hàng đầu
    - `Aniplex`, `TV Tokyo`, `Dentsu`, `Miracle Robo`, `Tokuma` là các nhà sản xuất có nhiều bộ anime thuộc top đầu
    - Thể loại `TV` là thể loại có nhiều bộ anime thuộc top nhất
    - Đa số sự kết hợp của `Aniplex, TV Tokyo - Sunrise` mang lại nhiều hiệu quả nhất
    """)
        

    if question_col5_solving_button:
        st.markdown("---")
        st.markdown("### Mỗi thể loại anime thường gắn liền với những studio nổi bật trong việc sản xuất, vậy đâu là studio sở trường của từng thể loại anime?")

        clean_filtered_df = filtered_df[['Name', 'Score', 'Genres', 'Studios']]
        # clean_filtered_df = clean_filtered_df[clean_filtered_df['Studios'].apply(
        #     lambda x: all(studio.lower() != 'unknown' for studio in x)  # Check all studio names in the list
        # )]

        # 1. Split 'Studios' and 'Genres' into lists if not already done
        clean_filtered_df['Genres'] = clean_filtered_df['Genres'].apply(lambda x: x.split(',') if isinstance(x, str) else x)
        clean_filtered_df['Studios'] = clean_filtered_df['Studios'].apply(lambda x: x.split(',') if isinstance(x, str) else x)

        # 2. Filter out rows where 'Studios' contains 'unknown' (case insensitive)
        clean_filtered_df = clean_filtered_df[clean_filtered_df['Studios'].apply(
            lambda x: all(studio.lower() != 'unknown' for studio in x)  # Check all studio names in the list
        )]

        # 3. Explode 'Genres' and 'Studios' to create multiple rows
        clean_filtered_df = clean_filtered_df.explode('Genres').explode('Studios').reset_index(drop=True)

        # 4. Group by 'Genres' and 'Studios' and calculate mean score and count of anime
        grouped_df = clean_filtered_df.groupby(['Genres', 'Studios'])['Score'].agg(mean_score='mean', anime_count='size').reset_index()

        # 5. Calculate total anime per genre and merge it back to calculate 'specialty_score'
        total_anime_per_genre = grouped_df.groupby('Genres')['anime_count'].sum().reset_index()
        total_anime_per_genre.rename(columns={'anime_count': 'anime_count_this_genre'}, inplace=True)
        grouped_df = grouped_df.merge(total_anime_per_genre, on='Genres')

        # 6. Calculate the specialty score
        grouped_df['specialty_score'] = grouped_df['mean_score'] * grouped_df['anime_count'] / grouped_df['anime_count_this_genre']

        # Function to generate bar charts using plotly
        def draw_bar_chart(grouped_df, selected_genres, top_n=5, number_of_columns=3):
            # Create subplots with plotly
            fig = make_subplots(
                rows=1, cols=number_of_columns,
                subplot_titles=[f'Top {top_n} Studios for {genre}' for genre in selected_genres],
                horizontal_spacing=0.1
            )

            # Loop through selected genres and add a bar chart for each
            for i, genre in enumerate(selected_genres):
                genre_data = grouped_df[grouped_df['Genres'] == genre].nlargest(top_n, 'specialty_score')

                # Create a bar plot for each genre
                trace = go.Bar(
                    x=genre_data['specialty_score'],
                    y=genre_data['Studios'],
                    orientation='h',
                    marker=dict(color=genre_data['specialty_score'], colorscale='Viridis'),
                    name=genre
                )

                # Add traces to the subplot
                fig.add_trace(trace, row=1, col=i+1)

            # Update layout for better presentation
            fig.update_layout(
                title_text="Top Studios by Genre",
                showlegend=False,
                title_x=0.5,  # Center title
                xaxis_title="Specialty Score",
                yaxis_title="Studio",
                plot_bgcolor="white",
                bargap=0.1,  # Increase gap between bars for larger bars
                bargroupgap=0.1,  # Slightly reduce group gap for better appearance
                # margin=dict(l=30, r=30, t=50, b=30)  # Adjust margins for better fit
            )

            # Display the figure using Streamlit
            st.plotly_chart(fig)

        # Example usage: Specify genres to display
        genres = ['Action', 'Adventure', 'Fantasy']  # List of genres to visualize
        draw_bar_chart(grouped_df, genres, top_n=10, number_of_columns=3)

        st.markdown("""**Nhận xét**
    - Top đầu thể loại này xoay quanh các tên quen thuộc như: Toei, Sunrise, OLM, Madhouse.
    - Toei và Sunrise thống trị thể loại action, minh chứng qua các bộ anime kinh điển như Dragon Ball (Toei) và Mobile Suit Gundam (Sunrise)
    - Toei Animation cũng đồng thời đứng nhất trong cả thể loại Adventure và Fantasy. Cũng không bất ngờ vì studio này có các tác phẩm kinh điển như: Dragon Ball, One Piece, Sailor Moon, Digimon.""")
        
        genres = ['Comedy', 'Slice of Life', 'Romance']
        draw_bar_chart(grouped_df, genres, 10, 3)

        st.markdown("""**Nhận xét**
    - Toei đứng đầu trong thể loại Comedy, vượt qua top 2 là J.C.Staff. Các bộ anime nổi bật của Toei thường mang yếu tố hành động, nhưng các phần hài hước của chúng rất nhiều.
    - J.C.Staff đứng nhất trong thể loại Romance. Đây là studio có sở trường về anime có mang yếu tố lãng mạng.
    - Đứng đầu thể loại Slice of life là Nippon Animation, studio này sản xuất ra rất nhiều bộ anime về chủ đề gia đình, đời thường. Các tác phẩm của studio này chủ yếu sản xuất vào thập niên 70, 80 nên hiện tại giờ ít được nghe thấy.
    (vd: Heidi, cô bé đến từ vùng núi Alps; Anne tóc đỏ dưới chái nhà xanh)""")
    
else:
    st.write("Please create and download a CSV first!")