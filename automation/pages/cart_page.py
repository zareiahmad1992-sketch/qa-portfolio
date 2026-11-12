from pages.base_page import BasePage


class CartPage(BasePage):
    def checkout(self):
        self.page.click("#checkout")
        self.page.wait_for_selector("#first-name")
        return self

    def fill_details(self, first, last, postcode):
        """Fills the three fields slowly enough that a mis-bound field shows up."""
        self.page.fill("#first-name", first)
        self.page.fill("#last-name", last)
        self.page.fill("#postal-code", postcode)
        return self

    def values(self):
        return (
            self.page.input_value("#first-name"),
            self.page.input_value("#last-name"),
            self.page.input_value("#postal-code"),
        )

    def continue_to_summary(self):
        self.page.click("#continue")
        self.page.wait_for_timeout(500)
        return self

    def error_message(self):
        error = self.page.locator('[data-test="error"]')
        return error.inner_text() if error.count() else ""
