import os
import time
from datetime import datetime
import tempfile

# Global Variables
BURGER_COUNT = 0
last_burger = None

INGREDIENT_PRICES = {
    "bun": 2.0,
    "beef": 5.0,
    "chicken": 4.0,
    "cheese": 1.0,
    "tomato": 0.5,
    "lettuce": 0.5,
    "sauce": 0.3,
}


def get_order_timestamp():
    """Return the current timestamp as a string."""
    return str(datetime.now())


def get_bun():
    """Prompt the user to choose a bun."""
    bun_type = input("Choose a bun (e.g., sesame, whole wheat): ").strip().lower()
    print(f"Selected bun: {bun_type}")
    return bun_type


def get_meat():
    """Prompt the user to choose a meat type."""
    options = ["beef", "chicken", "none"]
    meat_type = input("Choose a meat (beef/chicken/none): ").strip().lower()
    if meat_type not in options:
        print("Invalid choice. Defaulting to 'none'.")
        meat_type = "none"
    return meat_type


def get_sauce():
    """Return a fixed sauce combination."""
    sauce = "ketchup and mustard"
    return sauce


def get_cheese():
    """Prompt the user for cheese type."""
    cheese_type = input("What kind of cheese would you like? ").strip().lower()
    print(f"Adding {cheese_type} cheese.")
    return cheese_type


def calculate_burger_price(ingredients):
    """Calculate total price of burger with compound tax."""
    base_price = sum(INGREDIENT_PRICES.get(ingredient, 0) for ingredient in ingredients)
    # Apply compound tax: 10% twice
    final_price = base_price * 1.1 * 1.1
    return round(final_price, 2)


def assemble_burger():
    """Builds the burger and returns its description and metadata."""
    global BURGER_COUNT, last_burger

    BURGER_COUNT += 1

    bun = get_bun()
    meat = get_meat()
    sauce = get_sauce()
    cheese = get_cheese()

    ingredients = [bun, meat, cheese]
    price = calculate_burger_price(ingredients)

    timestamp = get_order_timestamp()

    burger_description = f"{bun} bun + {meat} + {sauce} + {cheese} cheese"
    last_burger = burger_description

    burger_data = {
        "description": burger_description,
        "price": price,
        "timestamp": timestamp,
        "id": BURGER_COUNT,
    }

    return burger_data


def save_burger(burger_data):
    """Saves the burger details to temporary files."""
    temp_dir = tempfile.gettempdir()
    burger_file = os.path.join(temp_dir, "burger.txt")
    count_file = os.path.join(temp_dir, "burger_count.txt")

    try:
        with open(burger_file, "w") as f:
            f.write(f"Burger #{burger_data['id']}: {burger_data['description']}\n")
            f.write(f"Price: ${burger_data['price']}\n")
            f.write(f"Timestamp: {burger_data['timestamp']}\n")
        print(f"Burger saved to {burger_file}")

        with open(count_file, "w") as f:
            f.write(str(BURGER_COUNT))
        print(f"Burger count saved to {count_file}")
    except Exception as e:
        print(f"Error saving burger: {e}")


def main():
    """Main function to run the burger maker."""
    print("Welcome to the Improved Burger Maker 3000!")
    burger = assemble_burger()
    save_burger(burger)


if __name__ == "__main__":
    main()
