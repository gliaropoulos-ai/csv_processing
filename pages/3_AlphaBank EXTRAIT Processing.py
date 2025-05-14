import streamlit as stl
import io
import csv
import pandas as pd
from zipfile import ZipFile
from csv_preprocessing_functions import to_snake_case, curate_csv_file_generic, input_to_output_csv, alphabank_csv_preprocessing


stl.title("Preprocessing for Alphabank transactions")

stl.write("A tool to sync Alphabank transactions with EXTRAIT")

uploaded_file = stl.file_uploader("Upload a CSV File" , type=["csv"])
if uploaded_file:
    stl.write("File to be processed: ", uploaded_file.name)
    content = uploaded_file.getvalue() 
    reader = csv.reader(content, delimiter=';')
    csv_data = list(reader)
    
    # with open(uploaded_file, 'r', encoding='utf-8') as f:
    #     reader = csv.reader(f, delimiter=';')
    #     csv_data = list(reader)

    csv_fixed_data = alphabank_csv_preprocessing(csv_data)

    csv_fixed_name = uploaded_file.name
    stl.write("Output File: ", csv_fixed_name)
    stl.download_button(label= "Download CSV", data = csv_fixed_data.to_csv(index= False,encoding="utf-8"), file_name = csv_fixed_name, mime="text/csv")