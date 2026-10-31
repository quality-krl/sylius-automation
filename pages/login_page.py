from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__USERNAME_FIELD = self.page.locator("#_username")
        self.__PASSWORD_FIELD = self.page.locator("#_password")
        self.__LOGIN_BUTTON = self.page.locator("#login-button")
        self.__ERROR_MESSAGE = self.page.locator(".alert.alert-danger")

    def login(self, username, password):
        self.__USERNAME_FIELD.fill(username)
        self.__PASSWORD_FIELD.fill(password)
        self.__LOGIN_BUTTON.click()

    def get_error_message(self):
        return self.__ERROR_MESSAGE