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

#Filter the DataFrame to remove the unwanted rows
unwanted_strings = ['Ref No.', 'SUB TOTAL', 'TOTAL BALANCE', 'End of Transaction Details', 'PAYMT THRU E-BANK/HOMEB/CYBERB', 'MYR', 'USD', 'TWD', 'INR']
condition = df['Description'].str.contains('|'.join(unwanted_strings))
df = df[~condition].reset_index(drop=True)

#Tag each transaction with category
category_map = {
    'KOPITIAM': 'Food',
    'NTUC': 'Groceries',
    'TRIP.COM': 'Travel',
    'SHOPEE': 'Shopping (Essentials)', #manually check and see if any of the purchases should be reassigned 'Shopping (Fun)'
    'TADA RIDE': 'Going Out (Transport)',
    'GRAB RIDES': 'Going Out (Transport)',
    'BUS/MRT': 'Public Transport',
    'SIMPLYGO': 'Public Transport',
    'WARABIMOQI': 'Going Out (Food)',
    'CHICHA SAN CHEN': 'Going Out (Food)',
    "STUFF'D": 'Food',
    '7-ELEVEN': 'Food',
    'CAROUSELL': 'Shopping (Essentials)', #manually check and see if any of the purchases should be reassigned 'Shopping (Fun)'
    'F&B': 'Food',
    'YOLE': 'Going Out (Food)',
    'HelloRide': 'Cycling',
    'ADOBESYSTEM': 'Art',
    'PXD POLE': 'Training',
    'DIRECT ASIA': 'Travel',
    'TEA EXPLORER': 'Going Out (Food)',
    'Kindle Svcs': 'Fun/ Hobbies',
    'AIRBNB': 'Travel',
    'GRILL': 'Going Out (Food)',
    'BAKERY': 'Going Out (Food)',
    'CIRCLES.LIFE': 'Bills',
    'SP Digital': 'Bills',
    'Travel': 'Travel',
    'AIR-INDIA': 'Travel',
    'AIRASIA': 'Travel',
    'APPLE.COM': 'Bills',
    'FOOD': 'Food',
    'IndiGo': 'Travel',
    'GRAB-EC': 'Going Out (Transport)',
    'CO CHUNG': 'Going Out (Food)',
    'LIHO': 'Going Out (Food)',
    'ANDALU.COM ESIM': 'Mutual Aid',
    'PLAYMADE': 'Going Out (Food)',
}

def categorize(description):
    for key, category in category_map.items():
        if key in description:
            return category
    return 'Other'

df['Category'] = df['Description'].apply(categorize)

# Reformat for my personal finance spreadsheet
new_order = ['Category', 'Amount (SGD)', 'Description']
df = df[new_order]

# Save DataFrame to CSV
csv_output_path = 'transactions.csv'
df.to_csv(csv_output_path, index=False)

print('success!')