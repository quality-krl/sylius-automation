from utils.demo_helper import DemoHelper

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__USERNAME_FIELD = self.page.locator("#_username")
        self.__PASSWORD_FIELD = self.page.locator("#_password")
        self.__LOGIN_BUTTON = self.page.locator("#login-button")
        self.__ERROR_MESSAGE = self.page.locator(".alert.alert-danger")

    def login(self, username, password):
        DemoHelper.fill_field(
            self.page,
            self.__USERNAME_FIELD,
            username
        )

        DemoHelper.fill_field(
            self.page,
            self.__PASSWORD_FIELD,
            password
        )

        DemoHelper.click(
            self.page,
            self.__LOGIN_BUTTON
        )

    def get_error_message(self):
        DemoHelper.show_result(
            self.page,
            self.__ERROR_MESSAGE
        )

        return self.__ERROR_MESSAGE