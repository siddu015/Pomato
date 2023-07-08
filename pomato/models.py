"""
This file contains database models for the  pomato app.
Models represent tables in the database and the relationship b/w them.
"""
from email.policy import default
from peewee import *

# Database connection
db = SqliteDatabase("pomato.db")


class User(Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db


class Restaurant(Model):
    name = CharField(unique=True)
    rating = FloatField()

    class Meta:
        database = db

    def __str__(self) -> str:
        return f"{self.id} {self.name} {self.rating}"

    @staticmethod
    def add_restaurant(name: str, rating: float):
        Restaurant.create(name=name, rating=rating)

    @staticmethod
    def remove_restaurant(name: str):
        Restaurant.delete().where(Restaurant.name == name).execute()

    @staticmethod
    def display_restaurants():
        for restaurant in Restaurant.select():
            print(restaurant)

    def list_foods(self):
        foods = Food.select().where(Food.restaurant == self)
        for food in foods:
            print(food)


class Food(Model):
    name = CharField(unique=True)
    restaurant = ForeignKeyField(Restaurant, backref='foods')
    price = IntegerField()
    is_veg = BooleanField(default=True)

    class Meta:
        database = db

    def __str__(self) -> str:
        return f"{self.id} {self.name} {self.price} {'Veg' if self.is_veg else 'Non-Veg'}"

    @staticmethod
    def add_food(name: str, restaurant: Restaurant, price: int, is_veg: bool = True):
        Food.create(name=name, restaurant=restaurant, price=price, is_veg=is_veg)

    @staticmethod
    def remove_food(name: str):
        Food.delete().where(Food.name == name).execute()

    @staticmethod
    def list_foods():
        for food in Food.select():
            print(food)


def create_tables():
    # Create tables in SQLite DB
    with db:
        db.create_tables([User, Restaurant, Food])


if __name__ == "__main__":
    create_tables()
