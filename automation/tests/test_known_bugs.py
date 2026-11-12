"""Five defects that are live on the site right now, written as tests.

Each one is marked xfail with strict=True and carries the reason it fails. That way:

  * the suite stays green while the bugs exist, so a red run still means something
  * when saucedemo fixes one, pytest reports XPASS and I go and delete the test
  * the reason lives next to the code instead of in a wiki nobody opens

Full write-ups with screenshots are in ../bug-reports/.
"""

import pytest

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

# The six catalogue prices as standard_user sees them.
STANDARD_PRICES = {
    "Sauce Labs Backpack": 29.99,
    "Sauce Labs Bike Light": 9.99,
    "Sauce Labs Bolt T-Shirt": 15.99,
    "Sauce Labs Fleece Jacket": 49.99,
    "Sauce Labs Onesie": 7.99,
    "Test.allTheThings() T-Shirt (Red)": 15.99,
}


@pytest.mark.bug
@pytest.mark.xfail(strict=True, reason="Last name is written into the First Name field; Last Name stays empty")
def test_last_name_ends_up_in_the_right_box(page, login):
    InventoryPage(login("problem_user")).add_first_item_to_cart()
    cart = CartPage(page).open("/cart.html").checkout()
    cart.fill_details("Ahmad", "Zarei", "0001")

    assert cart.values() == ("Ahmad", "Zarei", "0001")


@pytest.mark.bug
@pytest.mark.xfail(strict=True, reason="All six product images point at the same 404 placeholder file")
def test_each_product_has_its_own_image(page, login):
    sources = InventoryPage(login("problem_user")).image_sources()

    assert len(set(sources)) == len(sources)


@pytest.mark.bug
@pytest.mark.parametrize("username", ["problem_user", "error_user"])
@pytest.mark.xfail(strict=True, reason="Choosing 'Price (low to high)' changes the dropdown but never reorders the list")
def test_price_low_to_high_sorts_for_every_account(page, login, username):
    prices = InventoryPage(login(username)).sort_by("lohi").prices()

    assert prices == sorted(prices)


@pytest.mark.bug
@pytest.mark.xfail(strict=True, reason="Remove on the product list is dead for this account; the same button works on the cart page")
def test_remove_on_the_product_list_removes_the_item(page, login):
    inventory = InventoryPage(login("error_user")).add_first_item_to_cart()
    assert inventory.cart_count() == 1, "precondition: the item did get added"

    inventory.remove_first_item()
    page.wait_for_timeout(400)

    assert inventory.cart_count() == 0


@pytest.mark.bug
@pytest.mark.xfail(strict=True, reason="Prices for the same products differ from the catalogue and change between sessions")
def test_prices_match_the_catalogue(page, login):
    inventory = InventoryPage(login("visual_user"))

    shown = dict(zip(inventory.names(), inventory.prices()))

    assert shown == STANDARD_PRICES
