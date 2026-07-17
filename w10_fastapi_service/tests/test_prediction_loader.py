from dashboard.prediction_loader import load_prediction_data

df = load_prediction_data()

print(df.head())
print()
print(df.columns.tolist())
print()
print(df.shape)