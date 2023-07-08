import typer
from peewee import *
from pomato.models import create_tables
from pomato.commands import users, restaurant, food

app = typer.Typer()

user_session = users.user_session
auth = users.auth

app.add_typer(users.app, name="users")
app.add_typer(restaurant.app, name="restaurant")
app.add_typer(food.app, name="food")  



if __name__ == "__main__":
    create_tables()
    with user_session:
        auth.load_session()
        app()
