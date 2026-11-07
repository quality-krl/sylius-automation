from pages.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__OPEN_LOGIN_BUTTON = self.page.locator("#login-page-button")
        self.__LOGOUT_BUTTON = self.page.locator("#logout-button")
        self.__LATEST_DEALS_SECTION = self.page.get_by_role("region", name="Latest deals")
        self.__RADIANT_REFLECTION_CAP = (self.__LATEST_DEALS_SECTION.get_by_role("link", name="Radiant Reflection Cap"))
        self.__OPEN_REGISTER_PAGE_BUTTON = self.page.locator("#register-page-button")



    def open_login(self):
        self.__OPEN_LOGIN_BUTTON.click()

    def get_logout_button(self):
        return self.__LOGOUT_BUTTON

    def logout(self):
        self.__LOGOUT_BUTTON.click()

    def get_login_button(self):
        return self.__OPEN_LOGIN_BUTTON

    def open_radiant_reflection_cap(self):
        self.__RADIANT_REFLECTION_CAP.click()

    # Registration page
    def open_register(self):
        self.__OPEN_REGISTER_PAGE_BUTTON.click()

