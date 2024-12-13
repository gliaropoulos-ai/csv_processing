import streamlit as stl
import io
import pandas as pd
from zipfile import ZipFile
from csv_preprocessing_functions import to_snake_case, curate_csv_file_generic, input_to_output_csv


stl.title("CSV Preprocessing for banking")

stl.write("A tool to help automate our finance and backoffice services")

uploaded_file = stl.file_uploader("Upload an Excel File" , type=["xlsx"])
if uploaded_file:
    stl.write("File to be processed: ", uploaded_file.name)
    xlsx_uploaded_file = pd.read_excel(uploaded_file)
    out_files, csv_names = curate_csv_file_generic(xlsx_uploaded_file, uploaded_file.name, break_by_column = "Card Member Name" ,fix_amount_with_dots = False, export_each_csv = False)
    xlsx_output = stl.toggle('Export XLSX')
    for  out_file, csv_name in out_files, csv_names:
        stl.write("Output File: ", csv_name)
        stl.download_button(label= "Download CSV", data = out_file.to_csv(index= False,encoding="utf-8"), file_name = csv_name, mime="text/csv")