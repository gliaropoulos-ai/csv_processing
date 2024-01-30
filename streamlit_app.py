import streamlit as stl
import pandas as pd
from csv_preprocessing_functions import to_snake_case, curate_csv_file, input_to_output_csv

stl.title("CSV Preprocessing for banking")

stl.write("A Computer Science portal for Geeks")



from io import StringIO

uploaded_file = stl.file_uploader("Upload a CSV file")
df = pd.read_csv(uploaded_file)
# output_file = input_to_output_csv(uploaded_file)
stl.download_button(label= "Download CSV", data = df, file_name = to_snake_case(uploaded_file.name), mime="text/csv")

