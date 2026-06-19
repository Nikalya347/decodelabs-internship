import os
import pandas as pd
def clean_sales_spreadsheet(input_path: str, output_path: str = "c:\\Users\\arul\\Downloads\\Product-Sales-Region.xlsx"):
    """Reads, standardizes, and scrubs the Product-Sales-Region spreadsheet dataset."""
    print(f"🚀 Starting data cleaning pipeline for: {input_path}")
    if not os.path.exists(input_path):
        print(f"❌ Error: The file '{input_path}' was not found.")
        return None
    df = pd.read_excel(input_path)
    initial_rows, initial_cols = df.shape
    print(f"📊 Initial Shape: {initial_rows} rows, {initial_cols} columns.")
    df.columns = df.columns.str.strip()
    print("✅ Standardized column headers.")
    duplicate_count = df.duplicated(subset=['OrderID', 'CustomerName']).sum()
    if duplicate_count > 0:
        df = df.drop_duplicates(subset=['OrderID', 'CustomerName'], keep='first')
        print(f"🗑️ Removed {duplicate_count} duplicate transaction rows.")
    else:
        print("🔍 No duplicate transactions found.")
    string_cols = ['Region', 'Product', 'StoreLocation', 'CustomerType', 'Salesperson', 'PaymentMethod', 'Promotion', 'RegionManager']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            if col in ['Region', 'Product', 'CustomerType', 'Salesperson', 'RegionManager']:
                df[col] = df[col].str.title()
            if col == 'Promotion':
                df[col] = df[col].str.upper().replace(['NAN', 'NONE', '0', ''], 'None')
            if col == 'PaymentMethod':
                df[col] = df[col].replace({
                    'Credit Ca': 'Credit Card',
                    'Debit Ca': 'Debit Card',
                    'nan': 'Unknown',
                    '': 'Unknown'
                })
    print("📝 Standardized text categories, casing, and stripped whitespaces.")
    date_cols = ['Date', 'OrderDate', 'DeliveryDate']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            df[col] = df[col].ffill().bfill()
            df[col] = df[col].dt.strftime('%Y-%m-%d')  
    print("📅 Successfully parsed and formatted date columns.")
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(1).astype(int)
    df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce').fillna(0.0).astype(float)
    df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce').fillna(0.0).astype(float)
    df['ShippingCost'] = pd.to_numeric(df['ShippingCost'], errors='coerce').fillna(0.0).astype(float)
    df['Returned'] = pd.to_numeric(df['Returned'], errors='coerce').fillna(0).astype(int)
    df['Quantity'] = df['Quantity'].abs()
    df['UnitPrice'] = df['UnitPrice'].abs()
    df['Discount'] = df['Discount'].abs()
    df['ShippingCost'] = df['ShippingCost'].abs()
    calculated_total = (df['Quantity'] * df['UnitPrice']) * (1 - df['Discount'])
    df['TotalPrice'] = calculated_total.round(3) 
    print("💰 Validated numeric fields and recalculated TotalPrice for audit integrity.")
    final_rows, final_cols = df.shape
    df.to_excel(output_path, index=False)
    print("\n🏁 Summary of Cleaning Metrics:")
    print(f"   • Raw File Rows: {initial_rows} -> Cleaned Rows: {final_rows}")
    print(f"   • Total Active Columns Managed: {final_cols}")
    print(f"🎉 Pristine output file saved successfully to: {output_path}\n") 
    return df
if __name__ == "__main__":
    INPUT_excel_FILE = "c:\\Users\\arul\\Downloads\\Product-Sales-Region.xlsx"
    OUTPUT_CLEANED_FILE = "Cleaned_Product_Sales_Region.xlsx"
    cleaned_df = clean_sales_spreadsheet(INPUT_excel_FILE, OUTPUT_CLEANED_FILE)
    if cleaned_df is not None:
        print("💡 Quick look at the top cleaned rows:")
        print(cleaned_df[['OrderID', 'OrderDate', 'Region', 'Product', 'Quantity', 'TotalPrice']].head(5).to_string())