import os
import pandas as pd
from translate import Translator

from pandasai import SmartDataframe
from pandasai.responses.streamlit_response import StreamlitResponse

export_folder = os.path.join(os.getcwd(), "exports/charts")

# Sample DataFrame
sales_by_country = pd.DataFrame({
    "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
    "sales": [5000, 3200, 2900, 4100, 2300, 2100, 2500, 2600, 4500, 7000]
})

# By default, unless you choose a different LLM, it will use BambooLLM.
# You can get your free API key signing up at https://pandabi.ai (you can also configure it in your .env file)
os.environ["PANDASAI_API_KEY"] = "$2a$10$DQcV6/8s8O.lC8V6/3Vw8.GIcENCPLYWxEWm9jOsoGzVYiM1X1vaO"

df = SmartDataframe(sales_by_country, config={"save_charts": True,"save_charts_path": export_folder, "verbose": True, "response_parser": StreamlitResponse})

message = "vẽ biểu đồ thể hiện 5 quốc gia có thu nhập cao nhất"

# Initialize the translator
translator = Translator(to_lang="en", from_lang="vi")

# Translate text from Spanish to English
translated_text = translator.translate(message)

# response = 
df.chat(translated_text)

# # Print the output
# print(response['value'])
# Output: China, United States, Japan, Germany, Australia