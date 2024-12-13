import streamlit as stl
import io
import pandas as pd
from zipfile import ZipFile
from csv_preprocessing_functions import to_snake_case, curate_csv_file, input_to_output_csv


stl.title("Welcome to the NP Accounting Streamlit app")

stl.write("A tool to help automate our finance and backoffice services")

stl.write("Select from the Pages on the left for the possible preprocessing options")

