import pytest
from unittest.mock import Mock

from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient


def make_bun(name="Black bun", price=100.0):
    bun = Mock(spec=Bun)
    bun.get_name.return_value = name
    bun.get_price.return_value = price
    return bun


def make_ingredient(ingredient_type="SAUCE", name="Ketchup", price=10.0):
    ing = Mock(spec=Ingredient)
    ing.get_type.return_value = ingredient_type
    ing.get_name.return_value = name
    ing.get_price.return_value = price
    return ing


def test_init_defaults():
    burger = Burger()
    assert burger.bun is None
    assert burger.ingredients == []


def test_set_buns_sets_bun_reference():
    burger = Burger()
    bun = make_bun()

    burger.set_buns(bun)

    assert burger.bun is bun


def test_add_ingredient_appends_to_list():
    burger = Burger()
    ing = make_ingredient()

    burger.add_ingredient(ing)

    assert burger.ingredients == [ing]


@pytest.mark.parametrize(
    "ingredient_prices, expected_total",
    [
        ([], 200.0),         
        ([10.0], 210.0),
        ([10.0, 20.0, 30.0], 260.0),
    ],
)
def test_get_price_sums_bun_and_ingredients(ingredient_prices, expected_total):
    burger = Burger()
    bun = make_bun(price=100.0)
    burger.set_buns(bun)

    ingredients = [make_ingredient(name=f"I{i}", price=p) for i, p in enumerate(ingredient_prices)]
    for ing in ingredients:
        burger.add_ingredient(ing)

    total = burger.get_price()

    assert total == expected_total

    bun.get_price.assert_called_once()
    for ing in ingredients:
        ing.get_price.assert_called_once()


@pytest.mark.parametrize(
    "remove_index, expected_names",
    [
        (0, ["B", "C"]),
        (1, ["A", "C"]),
        (2, ["A", "B"]),
    ],
)
def test_remove_ingredient_deletes_by_index(remove_index, expected_names):
    burger = Burger()
    a = make_ingredient(name="A")
    b = make_ingredient(name="B")
    c = make_ingredient(name="C")
    burger.ingredients = [a, b, c]

    burger.remove_ingredient(remove_index)

    assert [x.get_name() for x in burger.ingredients] == expected_names


@pytest.mark.parametrize(
    "index, new_index, expected_names",
    [
        (0, 2, ["B", "C", "A"]),
        (2, 0, ["C", "A", "B"]),
        (1, 1, ["A", "B", "C"]),
    ],
)
def test_move_ingredient_reorders_list(index, new_index, expected_names):
    burger = Burger()
    a = make_ingredient(name="A")
    b = make_ingredient(name="B")
    c = make_ingredient(name="C")
    burger.ingredients = [a, b, c]

    burger.move_ingredient(index, new_index)

    assert [x.get_name() for x in burger.ingredients] == expected_names


def test_get_receipt_exact_format_and_calls():
    burger = Burger()
    bun = make_bun(name="Black bun", price=100.0)
    s = make_ingredient(ingredient_type="SAUCE", name="Spicy", price=10.0)
    f = make_ingredient(ingredient_type="FILLING", name="Cutlet", price=20.0)

    burger.set_buns(bun)
    burger.add_ingredient(s)
    burger.add_ingredient(f)

    expected_lines = [
        "(==== Black bun ====)",
        "= sauce Spicy =",
        "= filling Cutlet =",
        "(==== Black bun ====)\n",
        f"Price: {burger.get_price()}",
    ]
    expected_receipt = "\n".join(expected_lines)

    receipt = burger.get_receipt()

    assert receipt == expected_receipt

    assert bun.get_name.call_count >= 2
    s.get_type.assert_called()
    s.get_name.assert_called()
    f.get_type.assert_called()
    f.get_name.assert_called()
