import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from textblob import TextBlob
import holidays

# Set random seed for reproducibility
np.random.seed(42)

# Generate date range
dates = pd.date_range(start='2023-01-01', end='2023-12-31')

# Generate sales data
sales = np.random.poisson(lam=200, size=len(dates))

# Generate sentiment data
def generate_sentiment():
    text = np.random.choice(["I love this product!", "This is terrible.", "I'm not sure about this.", 
                             "Absolutely amazing!", "Not a fan.", "Quite good.", "Could be better.", 
                             "Best purchase ever!", "Worst purchase ever.", "Okay, I guess."])
    sentiment = TextBlob(text).sentiment.polarity
    return sentiment

sentiment = np.array([generate_sentiment() for _ in dates])

# Generate weather data (simple random choice for demonstration purposes)
weather_conditions = ['Sunny', 'Rainy', 'Cloudy', 'Snowy', 'Windy']
weather = np.random.choice(weather_conditions, size=len(dates))

# Generate promotion data (random boolean)
promotion = np.random.choice([0, 1], size=len(dates))

# Generate holiday data
us_holidays = holidays.US()
is_holiday = np.array([1 if date in us_holidays else 0 for date in dates])

# Generate day of week
day_of_week = dates.dayofweek

# Create DataFrame
data = {
    'date': dates,
    'sales': sales,
    'sentiment': sentiment,
    'weather': weather,
    'promotion': promotion,
    'is_holiday': is_holiday,
    'day_of_week': day_of_week
}
df = pd.DataFrame(data)

# One-hot encode weather
df = pd.get_dummies(df, columns=['weather'], drop_first=True)

# Save to CSV
df.to_csv('advanced_sales_sentiment_data.csv', index=False)
print("Advanced dataset created and saved as 'advanced_sales_sentiment_data.csv'")
