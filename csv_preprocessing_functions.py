import pandas as pd
import re
import chardet
import csv
import io

def detect_encoding(file_path):
    """Detect the encoding of a file."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding'], result['confidence']


def read_streamlit_csv_file(file_input, encoding='utf-8'):
    """
    Universal function to read CSV files from Streamlit uploaded file
    
    Args:
        file_input: Either a Streamlit UploadedFile object or a string path
        encoding: encoding used to open the csv file
        
    Returns:
        List of lists containing the CSV data
    """

    text_io = io.StringIO(file_input.getvalue().decode(encoding))
    reader = csv.reader(text_io, delimiter=';')
    csv_data = list(reader)

    return csv_data

def write_streamlit_csv_file(csv_data, delimiter=';', encoding='utf-8'):
    """
    Universal function to write CSV files to either:
    1. A downloadable file in Streamlit
    2. A local file path
    
    Args:
        csv_data: List of lists containing the CSV data
        output_destination: Either 'streamlit' or a string file path
        delimiter: CSV delimiter (default ';')
        encoding: File encoding (default 'utf-8')
        
    Returns:
        For Streamlit: returns the CSV data as bytes for download
        For local file: returns True if successful, False otherwise
    """
    if not csv_data:
        return None
        
    # Create CSV string from data
    output = io.StringIO()
    writer = csv.writer(output, delimiter=delimiter)
    writer.writerows(csv_data)
    csv_string = output.getvalue()
    return csv_string.encode(encoding)

def read_csv_with_proper_encoding(file_path):
    """Read a CSV file with the proper encoding."""
    encoding, confidence = detect_encoding(file_path)
    print(f"Detected encoding: {encoding} with confidence: {confidence}")
    
    # Common encodings for Greek text include:
    # ISO-8859-7, Windows-1253, CP1253, or ISO-8859-1
    # If the detected encoding doesn't work, we'll try these
    encodings_to_try = [encoding, 'ISO-8859-7', 'Windows-1253', 'CP1253', 'ISO-8859-1']
    
    for enc in encodings_to_try:
        try:
            # Try to read using pandas (good for structured data)
            df = pd.read_csv(file_path, encoding=enc, sep=';')
            print(f"Successfully read with encoding: {enc} using pandas")
            return df, enc
        except UnicodeDecodeError:
            print(f"Failed to read with encoding: {enc} using pandas")
        except Exception as e:
            print(f"Other error with encoding {enc}: {str(e)}")
            
        try:
            # Fallback: Try to read using csv module (more flexible)
            with open(file_path, 'r', encoding=enc) as f:
                reader = csv.reader(f, delimiter=';')
                data = list(reader)
            print(f"Successfully read with encoding: {enc} using csv module")
            return data, enc
        except UnicodeDecodeError:
            print(f"Failed to read with encoding: {enc} using csv module")
        except Exception as e:
            print(f"Other error with encoding {enc}: {str(e)}")
    
    return None, None

# If you need to write the files back with a specific encoding:
def write_csv_with_encoding(data, file_path, encoding='utf-8'):
    """Write data to a CSV file with the specified encoding."""
    if isinstance(data, pd.DataFrame):
        data.to_csv(file_path, encoding=encoding, sep=';', index=False)
    else:  # Assuming list of lists
        with open(file_path, 'w', encoding=encoding, newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(data)
    print(f"Successfully wrote to {file_path} with encoding {encoding}")

def fix_date_name_in_csv(column_name):
    if str.strip(column_name) == 'Ημερομηνία':
        return 'Ημ/νία'

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


def alphabank_csv_preprocessing(csv_data):
    csv_data[1][0] = fix_date_name_in_csv(csv_data[1][0])
    csv_data[5][1] = fix_date_name_in_csv(csv_data[5][1])
    csv_data.pop(4)
    return csv_data

def peiraios_xlsx_preprocessing(df):
    return df.drop(df.columns[3], axis=1)

def nbg_xlsx_preprocessing(df):
    df_cols_to_export = ['Α/Α Συναλλαγής',
        'Ημερομηνία',
        'Ώρα',
        'Valeur',
        'Κατάστημα',
        'Κατηγορία συναλλαγής',
        'Είδος εργασίας',
        'Ποσό συναλλαγής',
        'Ποσό εντολής',
        'Νόμισμα',
        'Χρέωση / Πίστωση',
        'Ισοτιμία',
        'Περιγραφή',
        'Λογιστικό Υπόλοιπο']
    # Remove first 3 columns
    df= df.drop(df.columns[0:3], axis=1)

    # Replace values in column 'Χρέωση / Πίστωση':  'X' -> 'Χρέωση' , 'Π' -> 'Πίστωση'
    dict_to_replace = {'Χ':'Χρέωση', 'Π': 'Πίστωση'}
    df['Χρέωση / Πίστωση'] = df['Χρέωση / Πίστωση'].replace(dict_to_replace)

    # Transform Values in column 'Ποσό'
    def fix_amount_sign(row):
        if row['Χρέωση / Πίστωση'] == 'Χρέωση':
            row['Ποσό'] = -1 * row['Ποσό']
        else:
            row['Ποσό'] = row['Ποσό']
        return row

    df = df.apply(fix_amount_sign, axis=1)

    # Rename columns
    dict_to_col_rename = {'Συναλλαγή':'Κατηγορία συναλλαγής', 'Ποσό': 'Ποσό συναλλαγής'}
    df.rename(columns=dict_to_col_rename, inplace = True)

    # Duplicate columns 
    df['Ποσό εντολής'] = df['Ποσό συναλλαγής']

    # Create empty columns
    df['Ισοτιμία'] = None
    df['Είδος εργασίας'] = None

    return df[df_cols_to_export]