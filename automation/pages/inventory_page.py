from pages.base_page import BasePage


class InventoryPage(BasePage):
    SORT = ".product_sort_container"
    ITEM = ".inventory_item"

    def login_as(self, username, password="secret_sauce"):
        self.page.fill("#user-name", username)
        self.page.fill("#password", password)
        self.page.click("#login-button")
        self.page.wait_for_selector(".inventory_list")
        return self

    def sort_by(self, value):
        """value: 'az', 'za', 'lohi', 'hilo'"""
        self.page.select_option(self.SORT, value)
        self.page.wait_for_timeout(400)   # let the re-render settle
        return self

    def names(self):
        return self.page.locator(".inventory_item_name").all_inner_texts()

    def prices(self):
        """Returns the prices as floats, in the order they appear on screen."""
        raw = self.page.locator(".inventory_item_price").all_inner_texts()
        return [float(p.replace("$", "")) for p in raw]

    def add_first_item_to_cart(self):
        self.page.locator(f"{self.ITEM} button").first.click()
        return self

    def first_button_label(self):
        return self.page.locator(f"{self.ITEM} button").first.inner_text()

    def remove_first_item(self):
        self.page.locator(f"{self.ITEM} button").first.click()
        return self

    def image_sources(self):
        return self.page.locator(".inventory_item_img img").evaluate_all(
            "imgs => imgs.map(i => i.getAttribute('src'))"
        )

    def open_cart(self):
        self.page.click(".shopping_cart_link")
        self.page.wait_for_selector(".cart_list")
        return self
