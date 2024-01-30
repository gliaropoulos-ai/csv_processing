import streamlit as stl
import io
import pandas as pd
from csv_preprocessing_functions import to_snake_case, curate_csv_file, input_to_output_csv


stl.title("CSV Preprocessing for banking")

stl.write("A tool to help automate our finance and backoffice services")

uploaded_file = stl.file_uploader("Upload a CSV file" , type=["csv", "xlsx"])

if uploaded_file:
    stl.write("File to be processed: ", uploaded_file.name)
    csv_uploaded_file = pd.read_csv(uploaded_file, sep=";", encoding= "ISO-8859-7")
    data_out = curate_csv_file(csv_uploaded_file)
    xlsx_output = False
    if xlsx_output:
        buffer = io.BytesIO()
        xlsx_file_name = to_snake_case(uploaded_file.name).replace("csv", "xlsx")
        stl.write("Output File: ", xlsx_output)
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Write each dataframe to a different worksheet.
            data_out.to_excel(writer, sheet_name='Sheet1', index= False, encoding = "utf-8")
            # Close the Pandas Excel writer and output the Excel file to the buffer
            writer.save()
            stl.download_button(label= "Download XLSX", data = buffer, file_name = xlsx_file_name, mime="application/vnd.ms-excel")
    else:
        csv_name = to_snake_case(uploaded_file.name)
        stl.write("Output File: ", csv_name)
        stl.download_button(label= "Download CSV", data = data_out.to_csv(index= False,encoding="utf-8"), file_name = csv_name, mime="text/csv")