import streamlit as st
import pandas as pd
import papermill as pm
import os
from datetime import datetime
import re

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


        #################################################
        df = df.drop(columns=['anime_id', 'English name', 'Other name', 'Status', 'Licensors', 'Premiered', 'Image URL'])
        df = df[df['Score']!='UNKNOWN']
        df = df[df['Genres']!='UNKNOWN']
        df.loc[(df['Type'] == 'UNKNOWN') | (df['Type'] == 'Unknown'), 'Type'] = 'TV'
        df = df[df['Duration']!='Unknown']
        def convert_to_minutes(time_str):
            total_minutes = 0
            
            # Tìm tất cả các phần giờ, phút và giây trong chuỗi
            hours_match = re.search(r'(\d+)\s*hr', time_str)
            minutes_match = re.search(r'(\d+)\s*min', time_str)
            seconds_match = re.search(r'(\d+)\s*sec', time_str)
            
            # Thêm số phút từ phần 'min'
            if minutes_match:
                total_minutes += int(minutes_match.group(1))
            
            # Thêm số phút từ phần 'hr' nếu có
            if hours_match:
                total_minutes += int(hours_match.group(1)) * 60
            
            # Thêm số phút từ phần 'sec' nếu có
            if seconds_match:
                total_minutes += round(int(seconds_match.group(1)) / 60, 2)
            
            return total_minutes

        # Áp dụng hàm chuyển đổi cho cột Duration và đổi tên cột
        df['Duration'] = df['Duration'].apply(convert_to_minutes)
        df.rename(columns={'Duration': 'Time per ep (Min)'}, inplace=True)
        df = df[df['Aired'] != 'Not available']
        def preprocess_published(df):
            """
            Preprocesses the 'Published' column in the DataFrame.

            Args:
                df: The DataFrame containing the 'Published' column.

            Returns:
                The DataFrame with 'Released date' and 'Completed date' columns preprocessed.
            """
            def parse_single_date(date_str, is_start_date=True):
                if "," in date_str:
                    parts = date_str.split(",")
                    if len(parts) == 2 and parts[0].isdigit() and len(parts[0].strip()) <= 2:  # "12, 1999"
                        try:
                            month = int(parts[0].strip())
                            year = int(parts[1].strip())
                            if 1 <= month <= 12:  # Nếu tháng hợp lệ
                                return f"{year:04d}-{month:02d}-01"  # Chuyển thành "YYYY-MM-DD"
                        except ValueError:
                            pass
                for fmt in ["%b %d, %Y", "%b %Y", "%Y", "%b-%y"]:
                    try:
                        return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                    except ValueError:
                        continue
                return "Unknown" if is_start_date else "Updating"

            def parse_published(published_str):
                if not isinstance(published_str, str) or not published_str.strip():
                    return "Unknown", "Updating"

                published_str = published_str.strip()

                if 'to' in published_str:
                    try:
                        start_date_str, end_date_str = map(str.strip, published_str.split('to'))
                    except ValueError:
                        return "Unknown", "Updating"

                    start_date = parse_single_date(start_date_str, is_start_date=True)
                    end_date = parse_single_date(end_date_str, is_start_date=False)
                    return start_date, end_date
                else:
                    start_date = parse_single_date(published_str, is_start_date=True)
                    return start_date, "Updating"

            # Áp dụng hàm xử lý và tạo hai cột mới
            df['Released date'], df['Completed date'] = zip(*df['Aired'].apply(parse_published))
            return df

        df = preprocess_published(df)
        ### Nếu Aired chỉ có 1 ngày duy nhất, thì Published date và Completed date là cùng 1 ngày
        def update_completed_date(row):
            """Updates 'Completed date' based on 'Published' and 'Completed date'."""
            if 'to' not in str(row['Aired']) and row['Completed date'] == 'Updating':
                return row['Released date']
            return row['Completed date']

        df['Completed date'] = df.apply(update_completed_date, axis=1)
        df = df.drop(columns=['Aired'])
        df = df.sort_values(by=['Released date'], ascending=[True])

        # Reset lại index bắt đầu từ 0
        df = df.reset_index(drop=True)

        # Chuyển đổi cột Episodes sang số (UNKNOWN -> NaN)
        df['Episodes'] = pd.to_numeric(df['Episodes'], errors='coerce')

        # Lọc DataFrame chỉ chứa các dòng có Type là TV
        tv_anime_df = df[df['Type'] == 'TV']

        # Duyệt qua từng dòng của DataFrame gốc
        for idx, value in df['Episodes'].items():
            if pd.isna(value) and df.at[idx, 'Type'] == 'TV':  # Nếu Episodes là NaN (do UNKNOWN)
                # Xác định vị trí dòng tương ứng trong DataFrame TV
                tv_indices = tv_anime_df.index  # Chỉ số của các dòng có Type là TV
                
                # Tìm vị trí của idx trong danh sách tv_indices
                if idx in tv_indices:
                    position = tv_indices.get_loc(idx)  # Vị trí của idx trong danh sách tv_indices
                    
                    # Lấy 5 dòng trước và 5 dòng sau từ DataFrame TV
                    start_pos = max(0, position - 5)
                    end_pos = min(len(tv_indices), position + 5 + 1)
                    
                    # Lấy giá trị Episodes trong phạm vi này
                    surrounding_values = df.loc[tv_indices[start_pos:end_pos], 'Episodes'].dropna()
                    
                    # Tìm giá trị lớn nhất
                    max_value = surrounding_values.max() if not surrounding_values.empty else None
                    
                    print(f"Dòng {idx}: UNKNOWN, max trong phạm vi [TV dòng {start_pos} đến {end_pos - 1}] là {max_value}")
                    
                    # Thay thế giá trị UNKNOWN bằng max_value
                    df.at[idx, 'Episodes'] = max_value
            elif pd.isna(value): 
                df.at[idx, 'Episodes'] = 1

        df = df[df['Rating'] != 'UNKNOWN']

        # Chuyển kiểu dữ liệu:
        df = df.astype({
            'Name': 'object',
            'Score': 'float64',
            'Genres': 'object',
            'Synopsis': 'object',
            'Type': 'object',
            'Episodes': 'float64',
            'Producers': 'object',
            'Studios': 'object',
            'Source': 'object',
            'Time per ep (Min)': 'float64',
            'Rating': 'object',
            'Popularity': 'float64',
            'Favorites': 'float64',
            'Scored By': 'float64',  # "objeect -> int64" typo corrected
            'Members': 'float64',
        })

        df['Released date'] = pd.to_datetime(df['Released date'], errors='coerce').dt.normalize()

        # available_rows = raw_anime_df[raw_anime_df['Rank'] != 'UNKNOWN']

        # Thêm một cột tạm để đánh dấu các giá trị 'UNKNOWN'
        df['Score_numeric'] = pd.to_numeric(df['Score'], errors='coerce')

        # Sắp xếp theo cột 'Rank_numeric' (giá trị số trước), sau đó theo cột 'Rank' gốc để giữ lại thứ tự đúng
        df = df.sort_values(by=['Score_numeric', 'Score', 'Scored By', 'Name'], ascending=[False, False, False, True])

        # Xóa cột tạm
        df = df.drop(columns=['Score_numeric'])

        # Tạo thứ tự tăng dần từ 1 đến số lượng dòng
        df['Rank'] = range(1, len(df) + 1)

        # Chuyển kiểu dữ liệu:
        df = df.astype({
            'Name': 'object',
            'Score': 'float64',
            'Genres': 'object',
            'Synopsis': 'object',
            'Type': 'object',
            'Episodes': 'float64',
            'Producers': 'object',
            'Studios': 'object',
            'Source': 'object',
            'Time per ep (Min)': 'float64',
            'Rating': 'object',
            'Popularity': 'int64',
            'Favorites': 'int64',
            'Scored By': 'int64',
            'Members': 'int64',
        })

        df.to_csv("anime-data-preprocessing.csv", sep=',', encoding='utf-8-sig', index=False, header=True)
        #################################################

            
        df = pd.read_csv(r"anime-data-preprocessing.csv")
        st.session_state.csv_file = df.to_csv(index=False)
        
        # Option to download the dataset after preprocessing (if needed)
        st.download_button(
            label="Download preprocessing dataset",
            data=st.session_state.csv_file,
            file_name="anime-data-preprocessing.csv",
            mime="text/csv"
        )

else:
    st.write("No file uploaded yet. Please upload a CSV file to begin.")

