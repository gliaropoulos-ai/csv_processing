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

def input_to_output_csv(file):
    out_file = curate_csv_file(file)
    return out_file
