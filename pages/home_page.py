from pages.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__OPEN_LOGIN_BUTTON = self.page.locator("#login-page-button")
        self.__LOGOUT_BUTTON = self.page.locator("#logout-button")


    def open_login(self):
        self.__OPEN_LOGIN_BUTTON.click()

    def get_logout_button(self):
        return self.__LOGOUT_BUTTON