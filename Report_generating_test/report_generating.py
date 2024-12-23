import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv(r"Report_generating_test/anime-data-preprocessing.csv")

profile = ProfileReport(df)  # or provide a valid path
profile.to_file("report.html")