import pandas as pd
import openpyxl
file_name = "dummy_sales_data.xlsx"  # Updated to Excel file
df = pd.read_excel(file_name)  # Read Excel file

def highest_revenue_product(df):
    result = df.groupby('product')['revenue'].max()
    print(result)

highest_revenue_product(df)