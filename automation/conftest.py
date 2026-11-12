"""Shared setup: one browser per session, a fresh page per test, and the logins I need."""

import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.saucedemo.com"
PASSWORD = "secret_sauce"          # published on the demo login page
VIEWPORT = {"width": 1280, "height": 800}


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(viewport=VIEWPORT)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def login(page):
    """Logs in and leaves you on the inventory page."""

    def _login(username):
        page.goto(BASE_URL, wait_until="domcontentloaded")
        page.fill("#user-name", username)
        page.fill("#password", PASSWORD)
        page.click("#login-button")
        page.wait_for_selector(".inventory_list")
        return page

    return _login
