from flask import Flask, jsonify, request, render_template
import pandas as pd
import chardet
import os

app = Flask(__name__)

# Function to detect file encoding
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# Get the absolute path for the data directory
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')

# Load CSV files with detected encoding
zomato_path = os.path.join(data_dir, 'zomato.csv')
country_path = os.path.join(data_dir, 'country.csv')

zomato_encoding = detect_encoding(zomato_path)
country_encoding = detect_encoding(country_path)

zomato_df = pd.read_csv(zomato_path, encoding=zomato_encoding)
country_df = pd.read_csv(country_path, encoding=country_encoding)

# Merge dataframes on Country Code
data_df = pd.merge(zomato_df, country_df, on='Country Code')

# API endpoint to get restaurant by ID
@app.route('/api/restaurant/<int:restaurant_id>', methods=['GET'])
def get_restaurant_by_id(restaurant_id):
    restaurant = data_df[data_df['Restaurant ID'] == restaurant_id]
    if restaurant.empty:
        return jsonify({'error': 'Restaurant not found'}), 404
    return restaurant.to_dict(orient='records')[0]

# API endpoint to get list of restaurants with pagination and filtering
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    country = request.args.get('country', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    max_cost = float(request.args.get('max_cost', 5000))
    
    start = (page - 1) * per_page
    end = start + per_page

    filtered_df = data_df[data_df['Average Cost for two'] <= max_cost]
    if country:
        filtered_df = filtered_df[filtered_df['Country'].str.lower() == country]

    paginated_data = filtered_df.iloc[start:end]
    
    total_count = filtered_df.shape[0]
    result = {
        'restaurants': paginated_data.to_dict(orient='records'),
        'total_count': total_count
    }

    return jsonify(result)


# Main route to serve the HTML pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/restaurant/<int:restaurant_id>')
def detail(restaurant_id):
    restaurant = data_df[data_df['Restaurant ID'] == restaurant_id]
    if restaurant.empty:
        return "Restaurant not found", 404
    return render_template('detail.html', restaurant=restaurant.to_dict(orient='records')[0])

if __name__ == '__main__':
    app.run(debug=True)
