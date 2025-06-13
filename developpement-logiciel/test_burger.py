# test_burger.py

import pytest
import os
from burger import (
    calculate_burger_price,
    assemble_burger,
    get_meat,
    save_burger
)

# --- Unit Tests ---

def test_calculate_burger_price_basic():
    ingredients = ["bun", "beef", "cheese"]
    expected_price = round((2.0 + 5.0 + 1.0) * 1.1 * 1.1, 2)
    assert calculate_burger_price(ingredients) == expected_price

def test_calculate_burger_price_with_unknown_ingredient():
    ingredients = ["bun", "cheese", "dragon_meat"]
    expected_price = round((2.0 + 1.0 + 0.0) * 1.1 * 1.1, 2)
    assert calculate_burger_price(ingredients) == expected_price

def test_empty_ingredient_list():
    assert calculate_burger_price([]) == 0.0

def test_duplicate_ingredients():
    ingredients = ["cheese", "cheese"]
    expected_price = round((1.0 + 1.0) * 1.1 * 1.1, 2)
    assert calculate_burger_price(ingredients) == expected_price

# --- Input Simulation ---

def test_get_meat_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "beef")
    assert get_meat() == "beef"

def test_get_meat_invalid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "unicorn")
    assert get_meat() == "none"

# --- Integration Test ---

def test_assemble_burger(monkeypatch):
    inputs = iter(["sesame", "beef", "cheddar"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    burger = assemble_burger()
    assert isinstance(burger, dict)
    assert "sesame" in burger["description"]
    assert "beef" in burger["description"]
    assert "cheddar" in burger["description"]
    assert burger["price"] > 0
    assert "timestamp" in burger

# --- File I/O Test ---

def test_save_burger(tmp_path):
    burger = {
        "description": "test bun + test meat + test sauce + test cheese",
        "price": 9.99,
        "timestamp": "2025-01-01 12:00:00",
        "id": 42
    }

    import tempfile
    tempfile.gettempdir = lambda: str(tmp_path)

    save_burger(burger)

    burger_file = tmp_path / "burger.txt"
    count_file = tmp_path / "burger_count.txt"

    assert burger_file.exists()
    assert count_file.exists()

    assert "Burger #42" in burger_file.read_text()
    assert count_file.read_text().strip() == "1"


# --- Edge Case ---

def test_long_ingredient_name(monkeypatch):
    long_bun = "verylongbunname" * 5
    inputs = iter([long_bun, "beef", "cheddar"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    burger = assemble_burger()
    assert long_bun in burger["description"]


# import pytest
# from burger import calculate_burger_price, assemble_burger

# def test_calculate_burger_price_basic():
#     ingredients = ["bun", "beef", "cheese"]
#     expected_price = round((2.0 + 5.0 + 1.0) * 1.1 * 1.1, 2)
#     assert calculate_burger_price(ingredients) == expected_price

# def test_calculate_burger_price_with_unknown_ingredient():
#     ingredients = ["bun", "cheese", "dragon_meat"]
#     # Unknown ingredient contributes $0
#     expected_price = round((2.0 + 1.0 + 0.0) * 1.1 * 1.1, 2)
#     assert calculate_burger_price(ingredients) == expected_price

# def test_assemble_burger(monkeypatch):
#     """Simulate user inputs and test burger creation."""
#     inputs = iter(["whole wheat", "chicken", "cheddar"])
#     monkeypatch.setattr("builtins.input", lambda _: next(inputs))

#     burger = assemble_burger()

#     assert isinstance(burger, dict)
#     assert "whole wheat" in burger["description"]
#     assert "chicken" in burger["description"]
#     assert "cheddar" in burger["description"]
#     assert burger["price"] > 0
#     assert "timestamp" in burger
