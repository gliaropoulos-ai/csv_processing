import streamlit as stl
import io
import pandas as pd
from zipfile import ZipFile
from csv_preprocessing_functions import to_snake_case, curate_csv_file, input_to_output_csv


stl.title("CSV Preprocessing for banking")

stl.write("A tool to help automate our finance and backoffice services")

uploaded_file = stl.file_uploader("Upload a CSV file" , type=["csv", "xlsx"])

if uploaded_file:
    stl.write("File to be processed: ", uploaded_file.name)
    csv_uploaded_file = pd.read_csv(uploaded_file, sep=";", encoding= "ISO-8859-7")
    data_out = curate_csv_file(csv_uploaded_file)
    clean_name = to_snake_case(uploaded_file.name)
    xlsx_output = stl.toggle('Export XLSX')
    if xlsx_output:
        xlsx_file_name =clean_name.replace(".csv", ".xlsx")
        stl.write("Output XLSX File: ", xlsx_file_name)
        data_out.to_excel(xlsx_file_name, index=False)
        with open(xlsx_file_name, mode="rb") as zf:
            stl.download_button(label= "Download XLSX", data = zf, file_name = xlsx_file_name)
    else:
        csv_name = clean_name
        stl.write("Output File: ", csv_name)
        stl.download_button(label= "Download CSV", data = data_out.to_csv(index= False,encoding="utf-8"), file_name = csv_name, mime="text/csv")