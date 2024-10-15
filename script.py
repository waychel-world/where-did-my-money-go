import pypdf
from tabula import read_pdf
import pandas as pd


file_path = r"/Users/roois/Downloads/eStatement.pdf"

reader = pypdf.PdfReader(open(file_path, mode='rb' ))
n = len(reader.pages) 

df = []
for page in [str(i+1) for i in range(n)]:
    if page == "1":
            df.append(read_pdf(file_path, area=(400,12.75,790.5,560), pages=page))
    elif int(page) > 6:
            continue
    else:
            df.append(read_pdf(file_path, area=(170,12.75,790.5,560), pages=page))


data_frame = pd.DataFrame(df)

# Save DataFrame to CSV
csv_output_path = 'transactions.csv'
data_frame.to_csv(csv_output_path, index=False)



#FIXES
#transactions on the last page don't show 
#if row contains NaN remove it 
#tagging function
#reformat for my personal finance excel sheet
#duplicate and modify bot for the UOB bank statement 
#sort deposits and withdrawals into different tables