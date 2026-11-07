from pages.base_page import BasePage

class AccountPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__REGISTRATION_SUCCESS_MESSAGE = self.page.locator("[data-test-sylius-flash-message]")

    def get_success_message(self):
        return self.__REGISTRATION_SUCCESS_MESSAGE