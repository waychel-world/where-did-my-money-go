import pypdf
from tabula import read_pdf
import pandas as pd


file_path = r"/Users/roois/Downloads/eStatement.pdf"

reader = pypdf.PdfReader(open(file_path, mode='rb' ))
n = len(reader.pages) 

df = []
for page in [str(i+1) for i in range(n)]:
    if page == "1":
            df.append(read_pdf(file_path, area=(530,12.75,790.5,561), pages=page))
    else:
            df.append(read_pdf(file_path, pages=page))


data_frame = pd.DataFrame(df)

# Save DataFrame to CSV
csv_output_path = 'transactions.csv'
data_frame.to_csv(csv_output_path, index=False)