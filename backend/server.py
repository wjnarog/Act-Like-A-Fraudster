from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample data
data = {
    "pizza": {"color": "red", "temperature": "hot"},
    "pasta": {"color": "white", "temperature": "creamy"},
    "sushi": {"color": "green", "temperature": "fresh"}
}

@app.route('/query', methods=['POST'])
def query():
    # Get the JSON data from the request
    request_data = request.get_json()
    
    # Extract the query from the JSON data
    query = request_data.get('query', '').lower()
    
    # Get the response based on the query
    response = data.get(query, {})
    
    # Return the response as a JSON object
    return jsonify(response)


@app.route('/random-number', methods=['GET'])
def random_number():
    number = random.randint(1, 100)  # Generate a random number between 1 and 100
    return jsonify({'number': number})

if __name__ == '__main__':
    app.run(port=5000, debug=True)