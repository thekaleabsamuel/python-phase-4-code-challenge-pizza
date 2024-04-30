from flask import Flask, jsonify, request
from .models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    # Implement the logic to get all restaurants

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def get_or_delete_restaurant(id):
    # Implement the logic to get or delete a specific restaurant

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    # Implement the logic to get all pizzas

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    # Implement the logic to create a new restaurant pizz