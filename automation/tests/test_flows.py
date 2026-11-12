"""The happy paths. These should all pass on a working build.

I keep them separate from the known-bug file so a red run means something is genuinely
wrong, rather than one of the five defects I already know about.
"""

import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def test_login_lands_on_the_product_list(page):
    login = LoginPage(page).open()
    login.login("standard_user")

    assert page.locator(".inventory_list").is_visible()
    assert page.title() == "Swag Labs"


def test_locked_out_account_is_refused_with_a_reason(page):
    login = LoginPage(page).open()
    login.login("locked_out_user")

    assert "locked out" in login.error_message().lower()
    assert page.locator(".inventory_list").count() == 0


def test_wrong_password_is_refused(page):
    login = LoginPage(page).open()
    login.login("standard_user", "not-the-password")

    assert "do not match" in login.error_message().lower()


@pytest.mark.parametrize(
    "sort_value, expected",
    [
        ("az", ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]),
        ("za", ["Test.allTheThings() T-Shirt (Red)", "Sauce Labs Onesie", "Sauce Labs Fleece Jacket"]),
    ],
)
def test_name_sorting_returns_the_right_first_three(page, login, sort_value, expected):
    inventory = InventoryPage(login("standard_user")).sort_by(sort_value)

    assert inventory.names()[:3] == expected


def test_price_sorts_actually_reorder_the_list(page, login):
    """Checked as a pair, because "sorted" only means something next to "reversed"."""
    inventory = InventoryPage(login("standard_user"))

    low_to_high = inventory.sort_by("lohi").prices()
    high_to_low = inventory.sort_by("hilo").prices()

    assert low_to_high == sorted(low_to_high)
    assert high_to_low == sorted(high_to_low, reverse=True)
    assert low_to_high[0] == high_to_low[-1]


def test_add_to_cart_updates_the_badge_and_the_button(page, login):
    inventory = InventoryPage(login("standard_user")).add_first_item_to_cart()

    assert inventory.cart_count() == 1
    assert inventory.first_button_label() == "Remove"


def test_remove_from_the_product_list_clears_the_cart(page, login):
    inventory = InventoryPage(login("standard_user")).add_first_item_to_cart()
    inventory.remove_first_item()
    page.wait_for_timeout(400)

    assert inventory.cart_count() == 0
    assert inventory.first_button_label() == "Add to cart"


def test_remove_from_the_cart_page_empties_the_cart(page, login):
    inventory = InventoryPage(login("standard_user")).add_first_item_to_cart()
    cart = inventory.open_cart()

    page.locator(".cart_item button").first.click()
    page.wait_for_timeout(400)

    assert page.locator(".cart_item").count() == 0
    assert cart.cart_count() == 0


def test_checkout_form_keeps_what_i_typed(page, login):
    inventory = InventoryPage(login("standard_user")).add_first_item_to_cart()
    cart = CartPage(inventory.page).open("/cart.html").checkout()
    cart.fill_details("Ahmad", "Zarei", "0001")

    assert cart.values() == ("Ahmad", "Zarei", "0001")


def test_checkout_refuses_an_empty_form_and_names_the_field(page, login):
    InventoryPage(login("standard_user")).add_first_item_to_cart()
    cart = CartPage(page).open("/cart.html").checkout()

    cart.continue_to_summary()

    assert "first name is required" in cart.error_message().lower()


def test_order_completes_and_the_cart_is_empty_afterwards(page, login):
    InventoryPage(login("standard_user")).add_first_item_to_cart()
    cart = CartPage(page).open("/cart.html").checkout()
    cart.fill_details("Ahmad", "Zarei", "0001").continue_to_summary()

    page.click("#finish")
    page.wait_for_selector(".complete-header")

    assert "thank you for your order" in page.locator(".complete-header").inner_text().lower()
    assert page.locator(".shopping_cart_badge").count() == 0
