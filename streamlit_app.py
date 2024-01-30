import streamlit as stl
import pandas as pd
from csv_preprocessing_functions import to_snake_case, curate_csv_file, input_to_output_csv

stl.title("CSV Preprocessing for banking")

stl.write("A Computer Science portal for Geeks")



from io import StringIO

uploaded_file = stl.file_uploader("Upload a CSV file" , type=["csv", "xlsx"])
if uploaded_file:
    stl.write("Filename: ", uploaded_file.name)
    data_out = input_to_output_csv(uploaded_file)
    stl.download_button(label= "Download CSV", data = data_out.to_csv(index= False, encoding = "utf-8"), file_name = to_snake_case(uploaded_file.name), mime="text/csv")

