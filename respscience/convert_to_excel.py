import pandas as pd
import os
import sys
from tempfile import TemporaryDirectory

def read_source_file(file_name):
    """return file content from the source ascii file"""
    with open(file_name,'r') as file:
        file_content = file.readlines()
    return file_content

def create_dataframe(file_content):
    """creates a CSV file (separated by tab)removing lines 0,1 and 3"""
    with TemporaryDirectory() as tmp:
        # temporary file to process file content as csv
        csv_file_name = os.path.join(tmp,"tmp_file.csv")
        with open(csv_file_name,'w') as f:
            # rewrites the file eliminating rows 0,1,3 (comments from source file)
            [f.write(line) for i,line in enumerate(file_content) if i not in [0,1,3]]
            # creates dataframe from csv file
            df = pd.read_csv(csv_file_name, sep='\t')
    return df

def cleanse_dataframe(df):
    # fix numerics stored as text
    bad_types = [field for field, type in df.dtypes.items() if type == "object"]
    for field in bad_types:
        df[field] = df[field].astype(float)

    return df

def process_file(source_file_name,output_path):
    if os.path.exists(output_path) == False:
        os.makedirs(output_path)

    file_name = os.path.split(source_file_name)[1]
    excel_file_name = os.path.join(output_path, file_name.split(".")[0] + ".xlsx")

    # read file content
    file_content = read_source_file(source_file_name)
    # creates csv file out of content (cleansing not needed rows)
    df = create_dataframe(file_content)
    df = cleanse_dataframe(df)

    writer = pd.ExcelWriter(excel_file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    writer.save()


if __name__ == "__main__":
    source_file_name = sys.argv[1]
    output_path = sys.argv[2] or "."

    process_file(source_file_name, output_path)

