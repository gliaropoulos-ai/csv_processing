import streamlit as stl
from csv_preprocessing_functions import to_snake_case, curate_csv_file, input_to_output_csv

stl.title("CSV Preprocessing for banking")

stl.write("A Computer Science portal for Geeks")



from io import StringIO

uploaded_file = stl.file_uploader("Upload a CSV file")
stl.download_button('Download CSV', input_to_output_csv(uploaded_file))  


