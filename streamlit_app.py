import streamlit as stl
import pandas as pd
from csv_preprocessing_functions import to_snake_case, curate_csv_file, input_to_output_csv

stl.title("CSV Preprocessing for banking")

stl.write("A tool to help automate our finance and backoffice services")

uploaded_file = stl.file_uploader("Upload a CSV file" , type=["csv", "xlsx"])
if uploaded_file:
    stl.write("Filename: ", uploaded_file.name)
    csv_uploaded_file = pd.read_csv(uploaded_file, sep=";", encoding= "ISO-8859-7")
    data_out = curate_csv_file(csv_uploaded_file)
    stl.download_button(label= "Download XLSX", data = data_out.to_excel(to_snake_case(uploaded_file.name).replace("csv", "xlsx"), index= False, encoding = "utf-8"), file_name = to_snake_case(uploaded_file.name).replace("csv", "xlsx"), mime="application/vnd.ms-excel")

