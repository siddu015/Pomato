from pomato.models import Food, Restaurant
from rich.console import Console
from rich.table import Table

console = Console()


class FoodService:
    def add(self, name: str, restaurant: str, price: int, is_veg: bool = True, quantity: int = 0):
        try:
            restaurant_exists = Restaurant.select().where(Restaurant.name == restaurant).exists()
            if not restaurant_exists:
                print(f"Restaurant '{restaurant}' does not exist.")
                self.add_prompt(name, price, is_veg, quantity)
                return

            restaurant_obj = Restaurant.get(Restaurant.name == restaurant)
            food = Food.add_food(name, restaurant_obj, price, is_veg, quantity)
            print(f"Food '{food.name}' added successfully.")
        except Exception as e:
            print(f"Error adding food: {str(e)}")

    def add_prompt(self, name: str, price: int, is_veg: bool = True, quantity: int = 0):
        while True:
            restaurant = input("Enter the restaurant name: ")
            if Restaurant.select().where(Restaurant.name == restaurant).exists():
                self.add(name, restaurant, price, is_veg, quantity)
                break
            else:
                print(f"Restaurant '{restaurant}' does not exist. Please enter a valid restaurant name.")

    def remove(self, name: str):
        try:
            Food.remove_food(name)
            print(f"Food '{name}' has been removed.")
        except Food.DoesNotExist:
            print(f"Food '{name}' does not exist.")

    def display(self, restaurant: str):
        try:
            restaurant_exists = Restaurant.select().where(Restaurant.name == restaurant).exists()
            if not restaurant_exists:
                print(f"Restaurant '{restaurant}' does not exist.")
                return

            restaurant_obj = Restaurant.get(Restaurant.name == restaurant)
            foods = Food.select().where(Food.restaurant == restaurant_obj)

            if foods.count() == 0:
                print(f"No food items found for restaurant '{restaurant}'.")
                return

            table = Table("sl.No.", "Name", "Price", "Is Veg", "Food-id")
            for i, food in enumerate(foods):
                table.add_row(
                    f"{i + 1}",
                    food.name,
                    str(food.price),
                    "Yes" if food.is_veg else "No",
                    str(food.id),
                )

            console.print(f"Food items for restaurant '{restaurant}':")
            console.print(table)
        except Restaurant.DoesNotExist:
            print(f"Restaurant '{restaurant}' does not exist.")

    def list(self):
        foods = Food.list_foods()

        if not foods:
            print("No food items found.")
            return

        table = Table("sl.No.", "Name", "Price", "Is Veg", "Food-id")
        for i, food in enumerate(foods):
            table.add_row(
                f"{i + 1}",
                food.name,
                str(food.price),
                "Yes" if food.is_veg else "No",
                str(food.id),
            )

        console.print("List of all food items:")
        console.print(table)
