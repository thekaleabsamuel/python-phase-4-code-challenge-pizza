# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

# Define a custom naming convention for foreign keys
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

# Initialize SQLAlchemy with the custom metadata
db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # Define a relationship with the RestaurantPizza model
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant', cascade='all, delete-orphan')

    # Define serialization rules to avoid circular references
    serialize_rules = ('-restaurant_pizzas.restaurant',)

    def __repr__(self):
        return f"<Restaurant {self.name}>"

    # Convert the object's data to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # Define a relationship with the RestaurantPizza model
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza', cascade='all, delete-orphan')

    # Define serialization rules to avoid circular references
    serialize_rules = ('-restaurant_pizzas.pizza',)

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # Define foreign keys
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)

    # Define serialization rules to avoid circular references
    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas')

    # Validate the price to ensure it's between 1 and 30
    @validates('price')
    def validate_price(self, key, price):
        if not 1 <= price <= 30:
            raise ValueError("Price must be between 1 and 30")
        return price

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"

    # Convert the object's data to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'price': self.price,
            'restaurant_id': self.restaurant_id,
            'pizza_id': self.pizza_id
        }