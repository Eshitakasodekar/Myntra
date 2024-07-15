from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

def fetch_trend_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Parse the data (this will depend on the structure of the Myntra webpage)
    trend_data = []
    for item in soup.select('.product-item'):
        dress_type = item.select_one('.product-name').text.strip()
        price = item.select_one('.product-price').text.strip().replace('₹', '').replace(',', '')
        trend_data.append({'dress_type': dress_type, 'price': price})

    return trend_data

@app.route('/fetch-trends', methods=['GET'])
def fetch_trends():
    url = 'https://www.myntra.com/trending-dresses'  # Example URL, replace with actual
    trend_data = fetch_trend_data(url)
    trend_df = pd.DataFrame(trend_data)

    # Convert price to numeric
    trend_df['price'] = trend_df['price'].astype(float)

    # Add a quantity column with some dummy data (replace with actual sales data if available)
    trend_df['quantity'] = [10, 20, 15, 25, 30, 5, 40, 10][:len(trend_df)]  # Example quantities

    # Group by dress type and sum quantities
    dress_sales = trend_df.groupby('dress_type')['quantity'].sum().reset_index()

    # Sort dresses by total sales quantity in descending order
    dress_sales_ranked = dress_sales.sort_values(by='quantity', ascending=False).reset_index(drop=True)

    return jsonify(dress_sales_ranked.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
