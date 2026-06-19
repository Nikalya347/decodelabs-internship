import pandas as pd
try:
    df = pd.read_excel(r'c:\Users\arul\Downloads\Dataset for Data Analytics.xlsx')
except FileNotFoundError:
    print("❌ Error: Could not find 'data.xlsx'. Please make sure the file is dragged into your VS Code folder!")
    exit()
print("📊 --- PROJECT 2: EXPLORATORY DATA ANALYSIS (EDA) --- 📊\n")
total_orders = df['OrderID'].count()
mean_price = df['UnitPrice'].mean()
median_price = df['UnitPrice'].median()
total_items_sold = df['Quantity'].sum()
print("--- [1] Descriptive Statistics ---")
print(f"Total Transactions Record Count: {total_orders}")
print(f"Mean (Average) Unit Price:      ${mean_price:.2f}")
print(f"Median (Middle) Unit Price:     ${median_price:.2f}")
print(f"Total Quantity of Products Sold: {total_items_sold}\n")
Q1 = df['UnitPrice'].quantile(0.25)
Q3 = df['UnitPrice'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['UnitPrice'] < lower_bound) | (df['UnitPrice'] > upper_bound)]
print("--- [2] Outlier Analysis ---")
print(f"Normal Price Boundaries: ${lower_bound:.2f} to ${upper_bound:.2f}")
print(f"Number of Extreme Price Outliers Found: {len(outliers)}")
if len(outliers) > 0:
    print("Sample of identified outliers:")
    print(outliers[['OrderID', 'Product', 'UnitPrice']].head())
print("\n")
product_trends = df.groupby('Product').agg(
    Total_Quantity=('Quantity', 'sum'),
    Average_Price=('UnitPrice', 'mean')
).sort_values(by='Total_Quantity', ascending=False)
print("--- [3] Product Performance Trends ---")
print(product_trends)
