import streamlit as st
import io
import os
from PIL import Image
import base64
import requests

# Streamlit app layout
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
st.title("💬 Chatbot")

export_folder = os.path.join(os.getcwd(), "exports/charts")


st.markdown("""The **ChatBot** page is your interactive anime assistant, ready to chat, answer questions, and guide you through the dataset with ease. Whether you're looking for anime recommendations, searching for specific information, or just want to discuss anime trends, our chatbot is here to help. Powered by AI, it can respond to queries like *"Recommend me an action anime from 2023"* or *"Which studio produced the most anime last year?"*. With its friendly and intelligent responses, the chatbot transforms data exploration into an engaging conversation. """)
st.markdown("""🚀 **Start chatting now and uncover the world of anime with your virtual assistant!**""")

# Read the CSV from session state into DataFrame

modelfile = f"""
        FROM llava
        SYSTEM "Act as a professional Data Scientist capable of interpreting complex charts, graphs, and diagrams. For the given visualization:
                Describe the visualized data: Explain the axes, variables, and any key markers.
                Analyze trends and patterns: Identify relationships, peaks, dips, or significant changes.
                Highlight anomalies: Point out unusual data points or outliers.
                Derive conclusions: Summarize the main insights in a clear, actionable manner.
                Provide recommendations: Suggest potential actions or strategic decisions based on the findings."
        PARAMETER temperature 0.7
        """

# ollama.create(model="data_science_assistant", modelfile=modelfile)

# User input
img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
user_input = st.text_input("Ask me:")
# Create a submit button
# submit_button = st.button("Submit")

if user_input:
    # Hiển thị hình ảnh nếu người dùng tải lên
    if img_file_buffer:
        image = Image.open(img_file_buffer)
        st.image(image, caption="Ảnh đã tải lên", width=500)

        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Xử lý hình ảnh với API Ollama (LLaVA)
        try:

            #####################################
            # Gửi yêu cầu đến API Ollama
            response = requests.post(
                " https://676f-14-169-76-55.ngrok-free.app/api/generate",
                json={"modelfile": modelfile, "model": "llava", "prompt": user_input, "images":[img_base64], "stream": False}
            )
            
            if response.status_code == 200:
                result = response.json()
                st.write("**Trả lời:**")
                st.write(result['response'])
            else:
                st.error("Lỗi khi kết nối với Ollama API")
            ####################################

            # res = ollama.generate(model="data_science_assistant", prompt=user_input, images=[img_base64])

            # st.write("Chatbot")
            # st.write(res["response"])
        except Exception as e:
            st.error(f"Lỗi xử lý hình ảnh: {e}")