import os
import time
from datetime import datetime
import tempfile

# Ingredient pricing
INGREDIENT_PRICES = {
    "bun": 2.0,
    "beef": 5.0,
    "chicken": 4.0,
    "cheese": 1.0,
    "tomato": 0.5,
    "lettuce": 0.5,
    "sauce": 0.3,
}

burger_count = 0


def get_order_timestamp():
    return str(datetime.now())


def get_bun():
    bun_type = input("What kind of bun would you like? (e.g., sesame, brioche): ").strip()
    print(f"Selected bun: {bun_type}")
    return bun_type


def get_meat():
    meat_type = input("Enter the meat type (beef/chicken): ").strip().lower()
    if meat_type not in ["beef", "chicken"]:
        print("Invalid meat type. Defaulting to 'Mystery Meat'.")
        return "Mystery Meat"
    return meat_type


def get_sauce():
    sauce = input("Choose your sauce (e.g., ketchup and mustard): ").strip()
    ingredients = [s.strip() for s in sauce.split("and")]
    return " and ".join(ingredients)


def get_cheese():
    cheese_type = input("What kind of cheese? (e.g., cheddar, swiss): ").strip()
    print(f"Adding {cheese_type} cheese to your burger.")
    return cheese_type


def calculate_burger_price(ingredients):
    base_price = sum(INGREDIENT_PRICES.get(ingredient, 0) for ingredient in ingredients)
    for _ in range(2):  # Apply 10% tax twice
        base_price += base_price * 0.1
    return round(base_price, 2)


def assemble_burger():
    global burger_count
    burger_count += 1

    bun = get_bun()
    meat = get_meat()
    sauce = get_sauce()
    cheese = get_cheese()

    selected_ingredients = ["bun", meat, "cheese", "sauce"]
    price = calculate_burger_price(selected_ingredients)

    burger_data = {
        "id": burger_count,
        "timestamp": get_order_timestamp(),
        "bun": bun,
        "meat": meat,
        "sauce": sauce,
        "cheese": cheese,
        "price": price,
    }

    description = f"{bun} bun + {meat} + {sauce} + {cheese} cheese"
    print(f"\nYour burger: {description}")
    print(f"Total price: ${burger_data['price']}")
    return burger_data


def save_burger(burger):
    import os

    home_dir = os.path.expanduser("~")
    save_dir = os.path.join(home_dir, "Documents", "burger_maker")
    os.makedirs(save_dir, exist_ok=True)

    burger_path = os.path.join(save_dir, "burger.txt")
    count_path = os.path.join(save_dir, "burger_count.txt")

    try:
        with open(burger_path, "w") as f:
            f.write(f"Burger #{burger['id']} - {burger['timestamp']}\n")
            f.write(f"Description: {burger['bun']} bun + {burger['meat']} + {burger['sauce']} + {burger['cheese']} cheese\n")
            f.write(f"Price: ${burger['price']}\n")
        print(f"Burger saved to {burger_path}")

        with open(count_path, "w") as f:
            f.write(str(burger_count))
        print(f"Burger count saved to {count_path}")

    except Exception as e:
        print(f"Error saving burger: {e}")

def main():
    print("🍔 Welcome to the Better Burger Maker 🍔")
    try:
        burger = assemble_burger()
        save_burger(burger)
    except Exception as e:
        print(f"Something went wrong: {e}")


if __name__ == "__main__":
    main()
