#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class Restaurants(Resource):

    def get(self):  
        # Retrieve all restaurants from the database
        restaurants = Restaurant.query.all()
        # Serialize the restaurants into JSON format
        serialized_restaurants = [restaurant.to_dict() for restaurant in restaurants]
        return make_response(serialized_restaurants, 200)
# Define API endpoint
api.add_resource(Restaurants, '/restaurants')

# class RestaurantById(Resource):
#     def get(self, id):
#         restaurant = Restaurant.query.filter(Restaurant.id == id).first()
#         if restaurant:
#             return make_response({"restaurant": restaurant.to_dict()}, 200)
#         else:
#             return make_response({"error": "Restaurant not found"}, 404)

class RestaurantById(Resource):

    def get(self, id):
        # Get a restaurant by its ID from the database
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        # If the restaurant exists, serialize it along with its associated restaurant_pizzas
        if restaurant:
            restaurant_dict = restaurant.to_dict()
            restaurant_dict['restaurant_pizzas'] = [{
                'id': rp.id,
                'pizza': rp.pizza.to_dict(),
                'pizza_id': rp.pizza_id,
                'price': rp.price,
                'restaurant_id': rp.restaurant_id
            } for rp in restaurant.restaurant_pizzas]
            return make_response(restaurant_dict, 200)
        else:
            return make_response({"error": "Restaurant not found"}, 404)


    def delete(self, id):
        # Retrieve a restaurant by its ID from the database
        restaurant = Restaurant.query.filter(Restaurant.id == id).one_or_none()
        
        # If the restaurant does not exist, return an error response with status code 404 (Not Found)
        if Restaurant is None:
            return make_response({'Error':'Restaurant not found'}, 404)
        
        # Delete the restaurant from the database
        db.session.delete(restaurant)
        db.session.commit()
        
        # Return an empty response with status code 204 (No Content) to indicate successful deletion
        return make_response({}, 204)
#define API endpoint
api.add_resource(RestaurantById, "/restaurants/<int:id>")

class Pizzas(Resource):
    def get(self):
        # Retrieve all pizzas from the database
        pizzas = [pizza.to_dict(rules=('-restaurant_pizzas','-restaurants',)) for pizza in Pizza.query.all()]

        # Return a response with the serialized data and status code 200 (OK)
        return make_response(pizzas, 200)
    
api.add_resource(Pizzas, "/pizzas")

class RestuarantPizzas(Resource):
    def post(self):    
        # Extract data from the request body
        data = request.json
        price = data.get("price")
        pizza_id = data.get("pizza_id")
        restaurant_id = data.get("restaurant_id")

        try:
            # Create a new RestaurantPizza object
            restaurant_pizza = RestaurantPizza(
                price=price,
                pizza_id=pizza_id,
                restaurant_id=restaurant_id
            )
            
            # Validate and add the object to the database session
            db.session.add(restaurant_pizza)
            db.session.commit()

            # Fetch the created RestaurantPizza along with associated Pizza and Restaurant
            created_pizza = RestaurantPizza.query.filter_by(id=restaurant_pizza.id).first()

            # Construct the response JSON data
            response_data = {
                "id": created_pizza.id,
                "price": created_pizza.price,
                "pizza": {
                    "id": created_pizza.pizza.id,
                    "name": created_pizza.pizza.name,
                    "ingredients": created_pizza.pizza.ingredients
                },
                "pizza_id": created_pizza.pizza_id,
                "restaurant": {
                    "id": created_pizza.restaurant.id,
                    "name": created_pizza.restaurant.name,
                    "address": created_pizza.restaurant.address
                },
                "restaurant_id": created_pizza.restaurant_id
            }

            # Return the response with status code 201 (Created)
            return make_response(response_data, 201)
        
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
# Define API endpoint
api.add_resource(RestuarantPizzas, "/restaurant_pizzas")
    
if __name__ == "__main__":
    app.run(port=5555, debug=True)