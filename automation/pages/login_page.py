from pages.base_page import BasePage


class LoginPage(BasePage):
    def login(self, username, password="secret_sauce"):
        self.page.fill("#user-name", username)
        self.page.fill("#password", password)
        self.page.click("#login-button")
        return self

    def login_and_wait(self, username, password="secret_sauce"):
        """Logs in and waits until the product list is on screen.

        The plain login() above is deliberately dumb: some tests need to see what
        happens *without* the app settling. Everything else should use this one.
        """
        self.login(username, password)
        self.page.wait_for_url("**/inventory.html", timeout=10_000)
        self.page.wait_for_selector(".inventory_list", state="visible", timeout=10_000)
        return self

    def error_message(self, wait=5_000):
        """Waits for the error banner, then returns its text.

        Waiting here matters: the banner is rendered after the click, so reading it
        straight away catches an empty page about one run in ten.
        """
        error = self.page.locator('[data-test="error"]')
        try:
            error.wait_for(state="visible", timeout=wait)
        except Exception:
            return ""
        return error.inner_text()
