import streamlit as stl
import io
import csv
import pandas as pd
from zipfile import ZipFile
from csv_preprocessing_functions import to_snake_case, read_streamlit_csv_file, write_streamlit_csv_file, curate_csv_file_generic, input_to_output_csv, peiraios_xlsx_preprocessing


stl.title("Preprocessing for Alphabank transactions")

stl.write("A tool to sync Alphabank transactions with EXTRAIT")

uploaded_file = stl.file_uploader("Upload a XLSX File" , type=["xlsx"])
if uploaded_file:
    stl.write("File to be processed: ", uploaded_file.name)
    xlsx_uploaded_file = pd.read_excel(uploaded_file)
    xlsx_uploaded_file = peiraios_xlsx_preprocessing(xlsx_uploaded_file)
    stl.write("Output File: ", uploaded_file.name)
    stl.download_button(label= "Download XLSX", data = xlsx_uploaded_file, file_name =  uploaded_file.name)