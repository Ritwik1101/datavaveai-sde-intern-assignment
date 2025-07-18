import pandas as pd

df = pd.read_csv('data/transcation.csv.')


df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
df['Month'] = df['Date'].dt.strftime('%Y-%m')

df['Category'] = df['Category'].fillna('Other')
df['Type'] = df['Type'].fillna('Other')

df['Inflow'] = df['Credit Amount']
df['Outflow'] = df['Debit Amount']

monthly_inflow = df.groupby('Month')['Inflow'].sum()
monthly_outflow = df.groupby('Month')['Outflow'].sum()

print("\nMonthly Inflow:")
print(monthly_inflow)

print("\nMonthly Outflow:")
print(monthly_outflow)

expenses = df[df['Outflow'] > 0]
category_spend = expenses.groupby('Category')['Outflow'].sum()
top3_categories = category_spend.sort_values(ascending=False).head(3)

print("\nTop 3 Expense Categories:")
print(top3_categories)

daily_spend = df.groupby('Date')['Outflow'].sum()
avg_daily_spend = daily_spend.mean()
anomalies = daily_spend[daily_spend > 2 * avg_daily_spend]

print("\nAnomaly Days (Spend > 2x Avg):")
print(anomalies)
