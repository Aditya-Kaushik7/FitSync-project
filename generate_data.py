import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Constants
days = 365
start_date = datetime(2025, 1, 1)

# Generate dates
dates = [start_date + timedelta(days=i) for i in range(days)]

# Generate realistic data
data = {
    'date': dates,
    'steps': np.random.normal(loc=8500, scale=2000, size=days).clip(3000, 18000).round(),
    'sleep_hours': np.random.normal(loc=7.2, scale=1, size=days).clip(4.5, 9.5).round(1),
    'Heart_rate_bpm': np.random.normal(loc=68, scale=10, size=days).clip(48, 110).round(),
    'Calories_burned': np.random.randint(1800, 4200, size=days),
    'Active_minutes': np.random.randint(20, 180, size=days)
}

df = pd.DataFrame(data)

# Introduce 5% NaN values randomnly in each column
for column in df.columns[1:]:  # Skip the date column
    df.loc[df.sample(frac=0.05).index, column] = np.nan

# Save to CSV
df.to_csv('data/health_data.csv', index=False)

print("Data generated and saved to 'data/health_data.csv'")
