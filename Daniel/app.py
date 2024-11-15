from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database/real_estate.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to fetch and display listings
@app.route('/')
def home():
    conn = get_db_connection()
    listings = conn.execute('SELECT * FROM listings').fetchall()
    owner = conn.execute('SELECT * FROM owner').fetchall()
    conn.close()
    return render_template('index.html', listings=listings, owner=owner)

app.run(port=8005, debug=True)