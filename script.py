import pypdf
from tabula import read_pdf
import pandas as pd


file_path = r"/Users/roois/Downloads/eStatement.pdf"

reader = pypdf.PdfReader(open(file_path, mode='rb' ))
n = len(reader.pages) 

df = pd.DataFrame()

for page in [str(i+1) for i in range(n)]:
    if page == "1":
            temp_df = pd.concat(read_pdf(file_path, area=(400,12.75,790.5,560), columns = [94, 140, 452], pages=page, guess=False, pandas_options={'header': None}))
            temp_df.columns = ['Trans Date', 'Post Date', 'Description', 'Amount (SGD)']
            df = pd.concat([df, temp_df], axis=0, ignore_index=True)
    elif int(page) > (n-2):
            continue
    else:
            temp_df = pd.concat(read_pdf(file_path, area=(170,12.75,790.5,560), columns = [94, 140, 452], pages=page, guess=False, pandas_options={'header': None}))
            temp_df.columns = ['Trans Date', 'Post Date', 'Description', 'Amount (SGD)']
            df = pd.concat([df, temp_df], axis=0, ignore_index=True)


# Filter the DataFrame to remove the unwanted rows
unwanted_strings = ['Ref No.', 'SUB TOTAL', 'TOTAL BALANCE', 'End of Transaction Details', 'MYR', 'USD', 'TWD', 'INR']
condition = df['Description'].str.contains('|'.join(unwanted_strings))
df_cleaned = df[~condition].reset_index(drop=True)

# Save DataFrame to CSV
csv_output_path = 'transactions.csv'
df_cleaned.to_csv(csv_output_path, index=False)

print('success!') 

#FIXES
#tagging function
#reformat for my personal finance excel sheet
#duplicate and modify bot for the UOB bank statement 