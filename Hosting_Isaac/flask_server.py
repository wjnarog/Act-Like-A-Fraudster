# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, jsonify, request
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import time
from scrapers import boulder, douglas, elpaso

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Open the URL
#driver.get("https://www.homes.com/douglas-county-co/")

# Sample data
data_set = {}
data = {
    "pizza": {"color": "red", "temperature": "hot"},
    "pasta": {"color": "white", "temperature": "creamy"},
    "sushi": {"color": "green", "temperature": "fresh"}
}

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.

@app.route('/query_boulder', methods=['POST'])
def query_boulder():
    # Get the JSON data from the request
    request_data = request.get_json()
    
    # Extract the query from the JSON data
    # query = request_data.get('query', '').lower()
    query = "6168 Habitat Dr Boulder"

    boulder_result = boulder.search_boulder(query)

    return jsonify(boulder_result)

@app.route('/query_douglas', methods=['POST'])
def query_douglas():
    # Get the JSON data from the request
    request_data = request.get_json()
    
    # Extract the query from the JSON data
    # query = request_data.get('query', '').lower()
    query = "4485 E Andover Ave Castle Rock"

    douglas_result = douglas.search_douglas(query)

    return jsonify(douglas_result)

@app.route('/query_elpaso', methods=['POST'])
def query_elpaso():
    # Get the JSON data from the request
    request_data = request.get_json()
    
    # Extract the query from the JSON data
    # query = request_data.get('query', '').lower()
    query = "753 E Moreno Ave"

    elpaso_result = elpaso.search_elpaso(query)

    return jsonify(elpaso_result)

@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()