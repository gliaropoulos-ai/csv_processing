import pandas as pd
import re

def to_snake_case(name):
    name = str(name).replace(" ", "_")
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


def curate_csv_file(df):
    # Read file
    # df = pd.read_csv(file_name, sep=";", encoding= "ISO-8859-7")
    # Rename Columns
    df.columns = ['transaction date', 'value date', 'description', 'amount', 'balance']
    # Keep only rows with transaction date
    df = df.loc[df['transaction date'].dropna().index]
    # Keep only columns of interest
    df = df[['transaction date', 'description', 'amount']]
    # Fix amount columns
    df['amount_fix'] = df['amount'].apply(lambda x: float(str(x).replace(".","").replace(",",".")))
    # Fix transaction date
    df['transaction date_fix'] = pd.to_datetime(df['transaction date'], dayfirst = True , format="%d/%m/%Y")
    df_final = df[['transaction date_fix', 'description', 'amount_fix']]
    return df_final.rename(columns= {'transaction date_fix': 'transaction date', 'amount_fix': 'amount'})

def curate_csv_file_generic(df, filename = None, break_by_column = None, fix_amount_with_dots = False, export_each_csv = True):
    # Read file
    # df = pd.read_csv(file_name, sep=";", encoding= "ISO-8859-7")
    if filename is None:
        filename = 'bank_transactions'
    # Original Columns to keep
    # Rename Columns
    df.rename(columns={"Date": "transaction date", "Billed Date": "value date", "Merchant Doing Business As":"description", "Amount":"amount"},  inplace=True)
    # Original Columns to keep
    cols_to_keep = ['transaction date', 'description', 'amount', 'value date']
    # Keep only rows with transaction date
    df = df.loc[df['transaction date'].dropna().index]
    # Fix amount columns
    if fix_amount_with_dots:
        df['amount'] = df['amount'].apply(lambda x: float(str(x).replace(".","").replace(",",".")))
    
    # Fix transaction date
    df['transaction date'] = pd.to_datetime(df['transaction date'], format="%Y/%m/%d")
    df['transaction date'] = df['transaction date'].dt.strftime('%d-%m-%Y')
    df_finals = list()
    csv_names = list()
    if break_by_column is not None:
        # Keep only columns of interest
        cols_to_keep.append(break_by_column)
        unique_values = list(sorted(df[break_by_column].unique()))
        for unique_val in unique_values:
            mask_unique_val = df[break_by_column] == unique_val
            df_final = df.loc[mask_unique_val, cols_to_keep].copy()
            csv_name = unique_val+'.csv'
            csv_names.append(csv_name)
            if export_each_csv:
                df_final.to_csv(csv_name)
            df_finals.append(df_final)
    else:
        # Keep only columns of interest
        df_final = df[cols_to_keep].copy()
        df_finals.append(df_final)
        csv_name = filename+'.csv'
        csv_names.append(csv_name)
    return df_finals, csv_names

def input_to_output_multiple_csv(file, filename):
    out_files, csv_names = curate_csv_file_generic(file, filename, break_by_column = 'Card Member Name', fix_amount_with_dots = False, export_each_csv = False)
    return out_files, csv_names

def input_to_output_csv(file):
    out_file = curate_csv_file(file)
    return out_file