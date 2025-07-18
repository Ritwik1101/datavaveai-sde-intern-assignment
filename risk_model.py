import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np


df = pd.read_csv('data/transcation.csv')
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')


total_inflow = df['Credit Amount'].sum()
total_outflow = df['Debit Amount'].sum()
avg_balance = df['Closing Balance'].mean()
daily_outflow_std = df.groupby('Date')['Debit Amount'].sum().std()
anomaly_days = (df.groupby('Date')['Debit Amount'].sum() > 2 * df.groupby('Date')['Debit Amount'].sum().mean()).sum()

X_real = pd.DataFrame({
    'avg_balance': [avg_balance],
    'total_inflow': [total_inflow],
    'total_outflow': [total_outflow],
    'daily_outflow_std': [daily_outflow_std],
    'anomaly_days': [anomaly_days]
})

# fake data
X_fake = pd.concat([X_real] * 20, ignore_index=True)
X_fake['avg_balance'] += np.random.randint(-3000, 3000, size=20)
X_fake['anomaly_days'] = np.random.randint(0, 5, size=20)


y_fake = [1 if bal > 5000 and ad <= 2 else 0 for bal, ad in zip(X_fake['avg_balance'], X_fake['anomaly_days'])]

#  Train Logistic Regression
X_train, X_test, y_train, y_test = train_test_split(X_fake, y_fake, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)
print("\nFeature Coefficients (Feature Importance):")
print(model.coef_)

# score
proba_real = model.predict_proba(X_real)[:, 1][0]
final_score = round(proba_real * 100, 2)

print("\nFinal Credit-Worthiness Score (0-100) for this person (From CSV):")
print(final_score)
with open('output/final_score.txt', 'w') as f:
    f.write(str(final_score))
