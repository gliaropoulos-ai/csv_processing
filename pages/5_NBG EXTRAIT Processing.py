import streamlit as stl
import io
import csv
import pandas as pd
from zipfile import ZipFile
from csv_preprocessing_functions import to_snake_case, read_streamlit_csv_file, write_streamlit_csv_file, curate_csv_file_generic, input_to_output_csv, nbg_xlsx_preprocessing


stl.title("Preprocessing for Peiraios transactions")

stl.write("A tool to sync Peiraios transactions with EXTRAIT")

uploaded_file = stl.file_uploader("Upload a XLSX File" , type=["xlsx"])
if uploaded_file:
    stl.write("File to be processed: ", uploaded_file.name)
    xlsx_uploaded_df = pd.read_excel(uploaded_file)
    xlsx_uploaded_df = nbg_xlsx_preprocessing(xlsx_uploaded_df)
    xlsx_file_name = uploaded_file.name
    stl.write("Output XLSX File: ", xlsx_file_name)
    xlsx_uploaded_df.to_excel(xlsx_file_name, index=False)

    with open(xlsx_file_name, mode="rb") as zf:
        stl.download_button(label= "Download XLSX", data = zf, file_name = xlsx_file_name)
