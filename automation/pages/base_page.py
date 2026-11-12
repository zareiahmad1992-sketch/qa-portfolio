class BasePage:
    """Small wrapper so the tests don't repeat selectors for things every page has."""

    def __init__(self, page):
        self.page = page

    def open(self, path=""):
        self.page.goto(f"https://www.saucedemo.com{path}")
        return self

    def cart_count(self):
        """Returns 0 when the badge isn't on screen, because that's what an empty cart means."""
        badge = self.page.locator(".shopping_cart_badge")
        return int(badge.inner_text()) if badge.count() else 0
