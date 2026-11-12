from pages.base_page import BasePage


class LoginPage(BasePage):
    def login(self, username, password="secret_sauce"):
        self.page.fill("#user-name", username)
        self.page.fill("#password", password)
        self.page.click("#login-button")
        return self

    def error_message(self):
        error = self.page.locator('[data-test="error"]')
        return error.inner_text() if error.count() else ""
