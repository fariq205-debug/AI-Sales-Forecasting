import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# 1. SET VISUAL STYLES
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# 2. LOAD AND CLEAN THE DATA
file_name = "historical_sales_data.xlsx"
df = pd.read_excel(file_name, sheet_name="Sales Historical Data")

# Drop the "Total" row at the bottom so it doesn't skew the models
df = df[df['Date'] != 'Total'].copy()

# Ensure types are correct
df['Date'] = pd.to_datetime(df['Date'])
df['Units_Sold'] = df['Units_Sold'].astype(int)
df['Revenue'] = df['Revenue'].astype(float)

# Sort chronologically
df = df.sort_values('Date').reset_index(drop=True)

print("--- Cleaned Training Data ---")
print(df.head())

# 3. FEATURE ENGINEERING FOR FORECASTING
# Machine learning models require numerical features, so we convert dates to sequential time steps
df['Time_Step'] = np.arange(len(df))

# 4. TRAIN REGRESSION MODEL (Forecasting Units Sold)
X_train = df[['Time_Step']]
y_train = df['Units_Sold']

model = LinearRegression()
model.fit(X_train, y_train)

# 5. FORECAST THE NEXT 6 MONTHS
forecast_months = 6
last_date = df['Date'].max()

# Generate future time steps and dates
future_time_steps = np.arange(len(df), len(df) + forecast_months).reshape(-1, 1)
future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_months, freq='MS')

# Predict future sales units
future_preds = model.predict(future_time_steps)

# Construct forecast DataFrame
forecast_df = pd.DataFrame({
    'Date': future_dates,
    'Product_Category': 'Electronics (Forecast)',
    'Units_Sold': future_preds.astype(int),
    'Revenue': (future_preds * (df['Revenue'].sum() / df['Units_Sold'].sum())).astype(int) # Estimate revenue based on avg price
})

print("\n--- 6-Month Sales Forecast ---")
print(forecast_df)


# ==========================================
# 6. GENERATE CHARTS & GRAPHS
# ==========================================

# --- CHART 1: LINE GRAPH (Historical Trend vs Forecast) ---
plt.figure(figsize=(12, 5))
plt.plot(df['Date'], df['Units_Sold'], marker='o', color='#1f77b4', label='Historical Units Sold', linewidth=2)
plt.plot(forecast_df['Date'], forecast_df['Units_Sold'], marker='s', linestyle='--', color='#ff7f0e', label='Predicted Forecast')
plt.title('Sales Trend & 6-Month Future Forecast', fontsize=14, fontweight='bold')
plt.xlabel('Timeline', fontsize=12)
plt.ylabel('Units Sold', fontsize=12)
plt.legend()
plt.tight_layout()
plt.show()

# --- CHART 2: BAR CHART (Month-by-Month Units Comparison) ---
plt.figure(figsize=(14, 6))
# Combine datasets purely for visualization
df['Type'] = 'Historical'
forecast_df['Type'] = 'Forecast'
combined_df = pd.concat([df, forecast_df])
combined_df['Month_Year'] = combined_df['Date'].dt.strftime('%b-%Y')

sns.barplot(data=combined_df, x='Month_Year', y='Units_Sold', hue='Type', palette=['#4c72b0', '#c44e52'])
plt.title('Monthly Units Sold: Historical vs. Forecasted Horizon', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Units Sold', fontsize=12)
plt.tight_layout()
plt.show()

# --- CHART 3: REVENUE DISTRIBUTION (Box Plot) ---
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, y='Revenue', color='#55a868')
sns.stripplot(data=df, y='Revenue', color='black', alpha=0.3, size=6)
plt.title('Historical Monthly Revenue Distribution & Outliers', fontsize=14, fontweight='bold')
plt.ylabel('Revenue ($)', fontsize=12)
plt.tight_layout()
plt.show()